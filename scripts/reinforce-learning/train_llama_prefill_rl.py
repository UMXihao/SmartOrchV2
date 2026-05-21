# train_llama_prefill_rl.py
import argparse
import json
import os
import random
import re
import subprocess
import time
from tqdm import tqdm
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Optional

import torch
import torch.nn as nn
import torch.optim as optim


# =========================
# 1. 配置
# =========================

@dataclass
class TrainConfig:
    llama_cli: str
    model_path: str
    prompt_file: str

    # 你的可选动作空间
    attn_heads_candidates: List[int]
    expert_candidates: List[int]

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
        self.prompts = cfg.prompt_file
        self.cache = self._load_cache(cfg.cache_path)

    @staticmethod
    def _load_prompts(path: str) -> List[str]:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

        text = p.read_text(encoding="utf-8")
        prompts = [x.strip() for x in text.split("\n\n") if x.strip()]
        if not prompts:
            raise ValueError("Prompt file is empty. Use blank lines to separate prompts.")
        return prompts

    @staticmethod
    def _load_cache(path: str) -> Dict[str, float]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cfg.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _build_base_cmd(self, prompt_file: str) -> List[str]:
        cmd = [
            self.cfg.llama_cli,
            "-m", self.cfg.model_path,
            "-f", prompt_file,
            "-n", str(self.cfg.n_predict),
            "-no-cnv"
        ]

        if self.cfg.threads is not None:
            cmd += ["-t", str(self.cfg.threads)]

        if self.cfg.ctx_size is not None:
            cmd += ["-c", str(self.cfg.ctx_size)]

        return cmd

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

        patterns = [
            r"prompt eval time\s*=\s*([0-9.]+)\s*ms",
            r"prompt\s+eval\s+time\s*:\s*([0-9.]+)\s*ms",
            r"prefill\s+time\s*=\s*([0-9.]+)\s*ms",
            r"prefill\s+latency\s*=\s*([0-9.]+)\s*ms",
        ]

        for pat in patterns:
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

    def _run_and_measure(self, prompt_file: str, heads: Optional[int], experts: Optional[int]) -> float:
        """
        heads=None, experts=None 表示默认参数，用于测 T。
        """
        cache_key = json.dumps({
            "prompt_hash": hash(prompt_file),
            "heads": heads,
            "experts": experts,
            "n_predict": self.cfg.n_predict,
            "threads": self.cfg.threads,
            "ctx_size": self.cfg.ctx_size,
        }, sort_keys=True)

        if cache_key in self.cache:
            return self.cache[cache_key]

        cmd = self._build_base_cmd(prompt_file)

        if heads is not None:
            cmd += ["--attn-heads", str(heads)]

        if experts is not None:
            override_value = self.cfg.override_kv_format.format(experts=experts)
            cmd += ["--override-kv", override_value]

        start = time.perf_counter()
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        end = time.perf_counter()

        if proc.returncode != 0:
            raise RuntimeError(
                "llama-cli failed.\n"
                f"Command: {' '.join(cmd)}\n"
                f"Return code: {proc.returncode}\n"
                f"stderr:\n{proc.stderr[-4000:]}"
            )

        parsed = self._parse_prefill_latency_seconds(proc.stderr, proc.stdout)

        # 优先使用 llama.cpp 日志里的 prompt eval time；
        # 如果解析不到，则退化为整个进程 wall time。
        latency = parsed if parsed is not None else (end - start)

        self.cache[cache_key] = latency
        self._save_cache()

        return latency

    def sample_prompt(self) -> str:
        return random.choice(self.prompts)

    def measure_default_T(self, prompt_file: str) -> float:
        return self._run_and_measure(prompt_file, heads=None, experts=None)

    def measure_action_latency(self, prompt_file: str, heads: int, experts: int) -> float:
        return self._run_and_measure(prompt_file, heads=heads, experts=experts)


# =========================
# 5. 强化学习环境
# =========================

class PrefillEnv:
    def __init__(self, cfg: TrainConfig, action_space: ActionSpace, runner: LlamaRunner):
        self.cfg = cfg
        self.action_space = action_space
        self.runner = runner

    def step(self, target_ratio: float, action_id: int) -> Dict:
        prompt = self.runner.prompts

        T = self.runner.measure_default_T(prompt)
        heads, experts = self.action_space.get(action_id)
        latency = self.runner.measure_action_latency(prompt, heads, experts)

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
    policy = PolicyNet(action_dim=len(actions))
    policy.load_state_dict(ckpt["model_state_dict"])
    policy.eval()

    state = torch.tensor([[target_ratio]], dtype=torch.float32)

    with torch.no_grad():
        logits, _ = policy(state)
        probs = torch.softmax(logits, dim=-1)[0]
        action_id = int(torch.argmax(probs).item())

    heads, experts = actions[action_id]

    print("Recommended parameters:")
    print(f"  target_ratio = {target_ratio}")
    print(f"  --attn-heads {heads}")
    print(f"  --override-kv deepseek2.expert_used_count={experts}")
    print()
    print("Full parameter fragment:")
    print(f"--attn-heads {heads} --override-kv deepseek2.expert_used_count={experts}")


# =========================
# 8. CLI
# =========================

def parse_int_list(s: str) -> List[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip()]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["train", "recommend"], required=True)

    parser.add_argument("--llama-cli", type=str, default="./llama-cli")
    parser.add_argument("--model", type=str, default="./model.gguf")
    parser.add_argument("--prompt-file", type=str, default="./prompts.txt")

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
        llama_cli=args.llama_cli,
        model_path=args.model,
        prompt_file=args.prompt_file,
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
        save_path=args.save_path,
        override_kv_format=args.override_kv_format,
    )

    if args.mode == "train":
        train(cfg)
    else:
        recommend(args.save_path, args.target_ratio)


if __name__ == "__main__":
    main()

'''
python train_llama_prefill_rl.py \
  --mode train \
  --llama-cli /home/lili-5090/Sean/SmartOrchV2/build/bin/llama-cli \
  --model /home/lili-5090/Sean/llama.cpp/models/deepseek-v2-lite-chat-q4_0.gguf \
  --prompt-file /home/lili-5090/Sean/SmartOrchV2/fix-long-token.txt \
  --attn-heads-candidates 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 \
  --expert-candidates 1,2,3,4,5,6 \
  --episodes 300 \
  --n-predict 1


python train_llama_prefill_rl.py \
  --mode recommend \
  --save-path prefill_policy.pt \
  --target-ratio 0.5
'''
