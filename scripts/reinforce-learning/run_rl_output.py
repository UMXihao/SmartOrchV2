import argparse
import subprocess
from typing import List

import torch
import torch.nn as nn

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

def parse_int_list(s: str) -> List[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip()]

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--save-path", type=str, default="prefill_policy.pt")
    parser.add_argument("--target-ratio", type=float, default=0.5)

    args = parser.parse_args()

    recommend(args.save_path, args.target_ratio)


if __name__ == "__main__":
    main()

'''
python run_rl_output.py \
  --save-path prefill_policy.pt \
  --target-ratio 0.5
'''
