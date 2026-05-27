# train_llama_prefill_rl_android.py
'''
python train_llama_prefill_rl_android.py \
  --mode train \
  --run-backend adb \
  --adb-workdir /data/local/tmp/demo \
  --llama-cli ./bin/llama-cli \
  --model ../models/deepseek-v2-lite-chat-q4_0.gguf \
  --prompt-file fix-token.txt \
  --device-prompt-file fix-token.txt \
  --attn-heads-candidates 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 \
  --expert-candidates 1,2,3,4,5,6 \
  --episodes 300 \
  --n-predict 1 \
  --cache-path latency_cache_phone.json \
  --result-log-path phone_train_trace.jsonl \
  --save-path prefill_policy_phone.pt
'''
import argparse
import hashlib
import json
import os
import random
import re
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm


# =========================
# 1. 配置
# =========================

@dataclass
class TrainConfig:
    # local: 直接在当前机器执行 llama-cli
    # adb:   在主机上训练，但每次测延迟都通过 adb shell 到手机执行 llama-cli
    run_backend: str

    llama_cli: str
    model_path: str
    prompt_file: str

    # adb 相关配置，仅 run_backend=adb 时使用
    adb_bin: str = "adb"
    adb_serial: Optional[str] = None
    adb_workdir: str = "/data/local/tmp/demo"
    adb_env: str = "LD_LIBRARY_PATH=lib"

    # 如果 device_prompt_file 不为空，则手机端 llama-cli 使用这个路径作为 -f 参数。
    # 如果为空且 adb_push_prompt=True，则脚本会把本机 prompt_file push 到 adb_workdir/prompts/ 下。
    # 如果为空且 adb_push_prompt=False，则直接把 prompt_file 原样传给手机端 -f。
    device_prompt_file: Optional[str] = None
    adb_push_prompt: bool = True

    # 你的可选动作空间
    attn_heads_candidates: List[int] = None
    expert_candidates: List[int] = None

    # llama-cli 通用推理参数
    n_predict: int = 1
    threads: Optional[int] = None
    ctx_size: Optional[int] = None

    # 训练参数
    episodes: int = 300
    lr: float = 3e-4
    gamma: float = 1.0

    # 训练时随机采样的目标延迟比例范围
    min_target_ratio: float = 0.35
    max_target_ratio: float = 0.90

    # reward 权重
    latency_penalty_weight: float = 3.0
    capacity_bonus_weight: float = 0.25

    # 缓存重复实验，避免同一组参数反复跑
    cache_path: str = "latency_cache.json"

    # 训练过程记录，每个 episode 写一行 json，便于后续分析手机端测量结果
    result_log_path: str = "phone_train_trace.jsonl"

    # 输出模型
    save_path: str = "prefill_policy.pt"

    # 根据你的 llama.cpp 修改情况调整
    # 官方 llama.cpp 的 override-kv 常见格式类似：key=type:value
    # 如果你的改造版本是 deepseek2.expert_used_count=4，就改成：
    # "deepseek2.expert_used_count={experts}"
    override_kv_format: str = "deepseek2.expert_used_count=int:{experts}"


# =========================
# 2. 动作空间
# =========================

class ActionSpace:
    def __init__(self, heads_list: List[int], expert_list: List[int]):
        self.actions: List[Tuple[int, int]] = []
        for h in heads_list:
            for e in expert_list:
                self.actions.append((h, e))

        if not self.actions:
            raise ValueError("Action space is empty.")

        self.max_heads = max(heads_list)
        self.max_experts = max(expert_list)

    def __len__(self):
        return len(self.actions)

    def get(self, action_id: int) -> Tuple[int, int]:
        return self.actions[action_id]

    def normalized_capacity(self, action_id: int) -> float:
        """
        用于 reward：在满足延迟约束的情况下，鼓励保留更多 heads/experts。
        """
        heads, experts = self.get(action_id)
        h_score = heads / self.max_heads
        e_score = experts / self.max_experts
        return 0.5 * h_score + 0.5 * e_score


# =========================
# 3. Policy 网络
# =========================

class PolicyNet(nn.Module):
    """
    输入状态：
        target_ratio，例如 0.5

    输出：
        每个 action 的概率分布
    """
    def __init__(self, action_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.policy_head = nn.Linear(64, action_dim)
        self.value_head = nn.Linear(64, 1)

    def forward(self, state: torch.Tensor):
        x = self.net(state)
        logits = self.policy_head(x)
        value = self.value_head(x)
        return logits, value


# =========================
# 4. llama-cli 调用与 prefill 延迟解析
# =========================

class LlamaRunner:
    def __init__(self, cfg: TrainConfig):
        self.cfg = cfg
        self.cache = self._load_cache(cfg.cache_path)
        self.host_prompt_file = cfg.prompt_file
        self.prompt_id = self._prompt_identity(cfg.prompt_file)
        self.device_prompt_file = self._prepare_prompt_file_for_backend()

    @staticmethod
    def _load_cache(path: str) -> Dict[str, float]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cfg.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _prompt_identity(path: str) -> str:
        """
        cache key 使用 prompt 文件内容 hash，避免 Python 内置 hash() 每次进程变化。
        如果 prompt 文件只在手机上，主机没有该文件，则退化为路径字符串。
        """
        p = Path(path)
        if p.exists() and p.is_file():
            data = p.read_bytes()
            return hashlib.sha1(data).hexdigest()
        return f"path:{path}"

    def _adb_cmd_prefix(self) -> List[str]:
        cmd = [self.cfg.adb_bin]
        if self.cfg.adb_serial:
            cmd += ["-s", self.cfg.adb_serial]
        return cmd

    def _run_adb_command(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if check and proc.returncode != 0:
            raise RuntimeError(
                "adb command failed.\n"
                f"Command: {' '.join(args)}\n"
                f"Return code: {proc.returncode}\n"
                f"stdout:\n{proc.stdout[-2000:]}\n"
                f"stderr:\n{proc.stderr[-2000:]}"
            )
        return proc

    def _prepare_prompt_file_for_backend(self) -> str:
        """
        local backend：直接使用主机 prompt_file。
        adb backend：
          1. 指定 --device-prompt-file：直接使用手机端路径；
          2. 未指定且 adb_push_prompt=True：把主机 prompt_file push 到手机 adb_workdir/prompts/；
          3. 未指定且 adb_push_prompt=False：把 prompt_file 原样传给手机端。
        """
        if self.cfg.run_backend == "local":
            return self.cfg.prompt_file

        if self.cfg.run_backend != "adb":
            raise ValueError(f"Unsupported run_backend: {self.cfg.run_backend}")

        if self.cfg.device_prompt_file:
            return self.cfg.device_prompt_file

        if not self.cfg.adb_push_prompt:
            return self.cfg.prompt_file

        host_prompt = Path(self.cfg.prompt_file)
        if not host_prompt.exists():
            raise FileNotFoundError(
                "Host prompt file not found. Either provide a valid local --prompt-file "
                "so the script can adb push it, or pass --device-prompt-file, or use --no-adb-push-prompt."
            )

        device_prompt_dir = f"{self.cfg.adb_workdir.rstrip('/')}/prompts"
        device_prompt_path = f"{device_prompt_dir}/{host_prompt.name}"

        self._run_adb_command(
            self._adb_cmd_prefix() + ["shell", f"mkdir -p {shlex.quote(device_prompt_dir)}"]
        )

        self._run_adb_command(
            self._adb_cmd_prefix() + ["push", str(host_prompt), device_prompt_path]
        )

        # 这里返回相对路径，配合 cd adb_workdir 后运行，命令更短。
        return f"prompts/{host_prompt.name}"

    def _build_llama_args(self, prompt_file: str) -> List[str]:
        cmd = [
            self.cfg.llama_cli,
            "-m", self.cfg.model_path,
            "-f", prompt_file,
            "-n", str(self.cfg.n_predict),
            "-no-cnv",
        ]

        if self.cfg.threads is not None:
            cmd += ["-t", str(self.cfg.threads)]

        if self.cfg.ctx_size is not None:
            cmd += ["-c", str(self.cfg.ctx_size)]

        return cmd

    def _build_shell_command_for_adb(self, llama_args: List[str]) -> str:
        """
        生成类似：
        cd /data/local/tmp/baseline && LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/xxx.gguf ...
        """
        quoted_llama_cmd = " ".join(shlex.quote(x) for x in llama_args)

        prefix = f"cd {shlex.quote(self.cfg.adb_workdir)}"
        if self.cfg.adb_env.strip():
            return f"{prefix} && {self.cfg.adb_env.strip()} {quoted_llama_cmd}"
        return f"{prefix} && {quoted_llama_cmd}"

    @staticmethod
    def _decode_subprocess_output(data) -> str:
        if data is None:
            return ""
        if isinstance(data, str):
            return data
        return data.decode("utf-8", errors="replace")

    def _run_llama(self, llama_args: List[str]) -> subprocess.CompletedProcess:
        if self.cfg.run_backend == "local":
            return subprocess.run(
                llama_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        if self.cfg.run_backend == "adb":
            shell_cmd = self._build_shell_command_for_adb(llama_args)
            adb_args = self._adb_cmd_prefix() + ["shell", shell_cmd]
            proc = subprocess.run(
                adb_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
            )
            return subprocess.CompletedProcess(
                args=proc.args,
                returncode=proc.returncode,
                stdout=self._decode_subprocess_output(proc.stdout),
                stderr=self._decode_subprocess_output(proc.stderr),
            )

        raise ValueError(f"Unsupported run_backend: {self.cfg.run_backend}")

    def _command_for_error_message(self, llama_args: List[str]) -> str:
        if self.cfg.run_backend == "adb":
            return " ".join(
                shlex.quote(x)
                for x in (self._adb_cmd_prefix() + ["shell", self._build_shell_command_for_adb(llama_args)])
            )
        return " ".join(shlex.quote(x) for x in llama_args)

    def _parse_prefill_latency_seconds(self, stderr: str, stdout: str) -> Optional[float]:
        """
        llama.cpp 常见日志类似：
            prompt eval time = 1234.56 ms / 100 tokens
        或：
            prompt eval time = 1.23 s / ...
        这里做了兼容解析。

        如果你的修改版日志格式不同，可以只改这个函数。
        """
        text = stderr + "\n" + stdout

        patterns_ms = [
            r"prompt eval time\s*=\s*([0-9.]+)\s*ms",
            r"prompt\s+eval\s+time\s*:\s*([0-9.]+)\s*ms",
            r"prefill\s+time\s*=\s*([0-9.]+)\s*ms",
            r"prefill\s+latency\s*=\s*([0-9.]+)\s*ms",
        ]

        for pat in patterns_ms:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                return float(m.group(1)) / 1000.0

        patterns_sec = [
            r"prompt eval time\s*=\s*([0-9.]+)\s*s",
            r"prefill\s+time\s*=\s*([0-9.]+)\s*s",
            r"prefill\s+latency\s*=\s*([0-9.]+)\s*s",
        ]

        for pat in patterns_sec:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                return float(m.group(1))

        return None

    def _run_and_measure(self, heads: Optional[int], experts: Optional[int]) -> float:
        """
        heads=None, experts=None 表示默认参数，用于测 T。
        """
        cache_key = json.dumps({
            "backend": self.cfg.run_backend,
            "adb_serial": self.cfg.adb_serial,
            "adb_workdir": self.cfg.adb_workdir,
            "adb_env": self.cfg.adb_env,
            "llama_cli": self.cfg.llama_cli,
            "model_path": self.cfg.model_path,
            "host_prompt_id": self.prompt_id,
            "device_prompt_file": self.device_prompt_file,
            "heads": heads,
            "experts": experts,
            "n_predict": self.cfg.n_predict,
            "threads": self.cfg.threads,
            "ctx_size": self.cfg.ctx_size,
            "override_kv_format": self.cfg.override_kv_format,
        }, sort_keys=True)

        if cache_key in self.cache:
            return self.cache[cache_key]

        cmd = self._build_llama_args(self.device_prompt_file)

        if heads is not None:
            cmd += ["--attn-heads", str(heads)]

        if experts is not None:
            override_value = self.cfg.override_kv_format.format(experts=experts)
            cmd += ["--override-kv", override_value]

        start = time.perf_counter()
        proc = self._run_llama(cmd)
        end = time.perf_counter()

        if proc.returncode != 0:
            raise RuntimeError(
                "llama-cli failed.\n"
                f"Backend: {self.cfg.run_backend}\n"
                f"Command: {self._command_for_error_message(cmd)}\n"
                f"Return code: {proc.returncode}\n"
                f"stdout:\n{proc.stdout[-4000:]}\n"
                f"stderr:\n{proc.stderr[-4000:]}"
            )

        parsed = self._parse_prefill_latency_seconds(proc.stderr, proc.stdout)

        # 优先使用 llama.cpp 日志里的 prompt eval time；
        # 如果解析不到，则退化为包含 adb 开销的整个进程 wall time。
        # 如果你希望训练目标严格是手机内核执行时间，应确保手机端日志能打印 prompt eval time。
        latency = parsed if parsed is not None else (end - start)

        self.cache[cache_key] = latency
        self._save_cache()

        return latency

    def measure_default_T(self) -> float:
        return self._run_and_measure(heads=None, experts=None)

    def measure_action_latency(self, heads: int, experts: int) -> float:
        return self._run_and_measure(heads=heads, experts=experts)


# =========================
# 5. 强化学习环境
# =========================

class PrefillEnv:
    def __init__(self, cfg: TrainConfig, action_space: ActionSpace, runner: LlamaRunner):
        self.cfg = cfg
        self.action_space = action_space
        self.runner = runner

    def step(self, target_ratio: float, action_id: int) -> Dict:
        T = self.runner.measure_default_T()

        heads, experts = self.action_space.get(action_id)
        latency = self.runner.measure_action_latency(heads, experts)

        latency_ratio = latency / max(T, 1e-9)
        target_latency = target_ratio * T

        satisfied = latency <= target_latency
        capacity = self.action_space.normalized_capacity(action_id)

        if satisfied:
            # 满足延迟约束：基础奖励 + 模型容量奖励
            reward = 1.0 + self.cfg.capacity_bonus_weight * capacity
        else:
            # 不满足延迟约束：按超出比例惩罚
            violation = (latency_ratio - target_ratio) / max(target_ratio, 1e-9)
            reward = -self.cfg.latency_penalty_weight * violation

        return {
            "reward": reward,
            "T": T,
            "target_ratio": target_ratio,
            "target_latency": target_latency,
            "latency": latency,
            "latency_ratio": latency_ratio,
            "satisfied": satisfied,
            "heads": heads,
            "experts": experts,
            "capacity": capacity,
        }


# =========================
# 6. 训练
# =========================

def append_result_log(path: Optional[str], record: Dict):
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def train(cfg: TrainConfig):
    random.seed(0)
    torch.manual_seed(0)

    action_space = ActionSpace(
        cfg.attn_heads_candidates,
        cfg.expert_candidates,
    )
    runner = LlamaRunner(cfg)
    env = PrefillEnv(cfg, action_space, runner)

    policy = PolicyNet(action_dim=len(action_space))
    optimizer = optim.Adam(policy.parameters(), lr=cfg.lr)

    print(f"Backend: {cfg.run_backend}")
    if cfg.run_backend == "adb":
        print(f"ADB workdir: {cfg.adb_workdir}")
        print(f"Device llama-cli: {cfg.llama_cli}")
        print(f"Device model: {cfg.model_path}")
        print(f"Device prompt: {runner.device_prompt_file}")
        print(f"ADB env: {cfg.adb_env}")

    print(f"Action count: {len(action_space)}")
    print("Actions:")
    for i, (h, e) in enumerate(action_space.actions):
        print(f"  {i:02d}: heads={h}, experts={e}")

    best_reward = -1e9

    for ep in tqdm(range(1, cfg.episodes + 1)):
        target_ratio = random.uniform(cfg.min_target_ratio, cfg.max_target_ratio)

        state = torch.tensor([[target_ratio]], dtype=torch.float32)

        logits, value = policy(state)
        dist = torch.distributions.Categorical(logits=logits)
        action_id = dist.sample()
        log_prob = dist.log_prob(action_id)

        result = env.step(target_ratio, int(action_id.item()))
        reward = torch.tensor([[result["reward"]]], dtype=torch.float32)

        # Advantage Actor-Critic 风格
        advantage = reward - value

        policy_loss = -log_prob * advantage.detach()
        value_loss = advantage.pow(2).mean()
        loss = policy_loss + 0.5 * value_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        log_record = {
            "episode": ep,
            "backend": cfg.run_backend,
            **result,
            "action_id": int(action_id.item()),
            "loss": float(loss.item()),
        }
        append_result_log(cfg.result_log_path, log_record)

        if result["reward"] > best_reward:
            best_reward = result["reward"]
            save_checkpoint(cfg.save_path, policy, action_space, cfg)

        if ep % 10 == 0 or ep == 1:
            print(
                f"[ep {ep:04d}] "
                f"target={result['target_ratio']:.2f}, "
                f"T={result['T']:.4f}s, "
                f"lat={result['latency']:.4f}s, "
                f"lat/T={result['latency_ratio']:.3f}, "
                f"heads={result['heads']}, "
                f"experts={result['experts']}, "
                f"ok={result['satisfied']}, "
                f"reward={result['reward']:.3f}"
            )

    save_checkpoint(cfg.save_path, policy, action_space, cfg)
    print(f"\nSaved policy to: {cfg.save_path}")
    if cfg.result_log_path:
        print(f"Saved train trace to: {cfg.result_log_path}")


def save_checkpoint(path: str, policy: PolicyNet, action_space: ActionSpace, cfg: TrainConfig):
    ckpt = {
        "model_state_dict": policy.state_dict(),
        "actions": action_space.actions,
        "config": cfg.__dict__,
    }
    torch.save(ckpt, path)


# =========================
# 7. 推理：输入 50%，输出参数
# =========================

def recommend(policy_path: str, target_ratio: float):
    ckpt = torch.load(policy_path, map_location="cpu")

    actions = [tuple(x) for x in ckpt["actions"]]
    cfg_dict = ckpt.get("config", {})
    override_kv_format = cfg_dict.get("override_kv_format", "deepseek2.expert_used_count=int:{experts}")

    policy = PolicyNet(action_dim=len(actions))
    policy.load_state_dict(ckpt["model_state_dict"])
    policy.eval()

    state = torch.tensor([[target_ratio]], dtype=torch.float32)

    with torch.no_grad():
        logits, _ = policy(state)
        probs = torch.softmax(logits, dim=-1)[0]
        action_id = int(torch.argmax(probs).item())

    heads, experts = actions[action_id]
    override_value = override_kv_format.format(experts=experts)

    print("Recommended parameters:")
    print(f"  target_ratio = {target_ratio}")
    print(f"  --attn-heads {heads}")
    print(f"  --override-kv {override_value}")
    print()
    print("Full parameter fragment:")
    print(f"--attn-heads {heads} --override-kv {override_value}")


# =========================
# 8. CLI
# =========================

def parse_int_list(s: str) -> List[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip()]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["train", "recommend"], required=True)

    parser.add_argument(
        "--run-backend",
        choices=["local", "adb"],
        default="local",
        help="local means run llama-cli on this machine; adb means run llama-cli on Android through adb shell.",
    )

    # local backend 默认值沿用旧脚本；
    # adb backend 推荐显式传入 ./bin/llama-cli 和 ../models/xxx.gguf
    parser.add_argument("--llama-cli", type=str, default="./llama-cli")
    parser.add_argument("--model", type=str, default="./model.gguf")
    parser.add_argument("--prompt-file", type=str, default="./prompts.txt")

    parser.add_argument("--adb-bin", type=str, default="adb")
    parser.add_argument("--adb-serial", type=str, default=None)
    parser.add_argument("--adb-workdir", type=str, default="/data/local/tmp/demo")
    parser.add_argument("--adb-env", type=str, default="LD_LIBRARY_PATH=lib")
    parser.add_argument("--device-prompt-file", type=str, default=None)
    parser.add_argument(
        "--no-adb-push-prompt",
        action="store_true",
        help="Do not push local prompt file to Android. Use prompt-file or device-prompt-file as already existing device path.",
    )

    parser.add_argument("--attn-heads-candidates", type=str, default="4,8,12,16,24,32")
    parser.add_argument("--expert-candidates", type=str, default="1,2,4,6,8")

    parser.add_argument("--n-predict", type=int, default=1)
    parser.add_argument("--threads", type=int, default=None)
    parser.add_argument("--ctx-size", type=int, default=None)

    parser.add_argument("--episodes", type=int, default=300)
    parser.add_argument("--lr", type=float, default=3e-4)

    parser.add_argument("--min-target-ratio", type=float, default=0.35)
    parser.add_argument("--max-target-ratio", type=float, default=0.90)

    parser.add_argument("--cache-path", type=str, default="latency_cache.json")
    parser.add_argument("--result-log-path", type=str, default="phone_train_trace.jsonl")
    parser.add_argument("--save-path", type=str, default="prefill_policy.pt")

    parser.add_argument(
        "--override-kv-format",
        type=str,
        default="deepseek2.expert_used_count=int:{experts}",
        help=(
            "Format for override-kv. "
            "Example official style: deepseek2.expert_used_count=int:{experts}; "
            "custom style: deepseek2.expert_used_count={experts}"
        ),
    )

    parser.add_argument("--target-ratio", type=float, default=0.5)

    args = parser.parse_args()

    cfg = TrainConfig(
        run_backend=args.run_backend,
        llama_cli=args.llama_cli,
        model_path=args.model,
        prompt_file=args.prompt_file,
        adb_bin=args.adb_bin,
        adb_serial=args.adb_serial,
        adb_workdir=args.adb_workdir,
        adb_env=args.adb_env,
        device_prompt_file=args.device_prompt_file,
        adb_push_prompt=not args.no_adb_push_prompt,
        attn_heads_candidates=parse_int_list(args.attn_heads_candidates),
        expert_candidates=parse_int_list(args.expert_candidates),
        n_predict=args.n_predict,
        threads=args.threads,
        ctx_size=args.ctx_size,
        episodes=args.episodes,
        lr=args.lr,
        min_target_ratio=args.min_target_ratio,
        max_target_ratio=args.max_target_ratio,
        cache_path=args.cache_path,
        result_log_path=args.result_log_path,
        save_path=args.save_path,
        override_kv_format=args.override_kv_format,
    )

    if args.mode == "train":
        train(cfg)
    else:
        recommend(args.save_path, args.target_ratio)


if __name__ == "__main__":
    start = time.time()
    print("************ start time:", start, " ************")
    main()
    end = time.time()
    print("************ end time:", end, " ************")
    print("************ train time:", end - start, " ************")


'''
示例 1：手机端 prompt 由脚本自动 push 到 /data/local/tmp/baseline/prompts/
python train_llama_prefill_rl_android.py \
  --mode train \
  --run-backend adb \
  --adb-workdir /data/local/tmp/baseline \
  --llama-cli ./bin/llama-cli \
  --model ../models/deepseek-v2-lite-chat-q4_0.gguf \
  --prompt-file /home/lili-5090/Sean/SmartOrchV2/fix-long-token.txt \
  --attn-heads-candidates 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 \
  --expert-candidates 1,2,3,4,5,6 \
  --episodes 300 \
  --n-predict 1 \
  --cache-path latency_cache_phone.json \
  --result-log-path phone_train_trace.jsonl \
  --save-path prefill_policy_phone.pt

示例 2：如果 prompt 文件已经在手机上，例如 /data/local/tmp/baseline/fix-long-token.txt
python train_llama_prefill_rl_android.py \
  --mode train \
  --run-backend adb \
  --adb-workdir /data/local/tmp/baseline \
  --llama-cli ./bin/llama-cli \
  --model ../models/deepseek-v2-lite-chat-q4_0.gguf \
  --prompt-file fix-long-token.txt \
  --device-prompt-file fix-long-token.txt \
  --attn-heads-candidates 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 \
  --expert-candidates 1,2,3,4,5,6 \
  --episodes 300 \
  --n-predict 1 \
  --cache-path latency_cache_phone.json \
  --result-log-path phone_train_trace.jsonl \
  --save-path prefill_policy_phone.pt

推理推荐：
python train_llama_prefill_rl_android.py \
  --mode recommend \
  --save-path prefill_policy_phone.pt \
  --target-ratio 0.5
'''
