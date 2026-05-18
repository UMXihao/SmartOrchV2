import requests
from tqdm import tqdm
from datasets import load_dataset

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

# 加载 AlpacaEval 数据集
ALPACA_EVAL_URL = (
    "https://huggingface.co/datasets/tatsu-lab/alpaca_eval/resolve/main/alpaca_eval.json"
)

alpaca_eval = load_dataset(
    "json",
    data_files=ALPACA_EVAL_URL,
    split="train",
)

# for i in tqdm(range(len(alpaca_eval))):
for i in tqdm(range(100)):
    # 如果只想触发前 100 条，可以改成：
    # for i in tqdm(range(100)):

    instruction = alpaca_eval[i]["instruction"]

    # 构造 AlpacaEval 指令跟随 prompt
    input_text = (
        "Below is an instruction. Write a response that appropriately completes the request.\n\n"
        f"### Instruction:\n{instruction}\n\n"
        "### Response:\n"
    )

    data = {
        "prompt": input_text,
        "n_predict": 512,
        "stop": ["### Instruction:", "\n\n### Instruction:"]
    }

    requests.post(url, headers=headers, json=data)
