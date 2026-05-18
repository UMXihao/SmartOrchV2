import requests
from tqdm import tqdm
from datasets import load_dataset

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

mtbench = load_dataset(
    "json",
    data_files="https://huggingface.co/spaces/lmsys/mt-bench/raw/main/data/mt_bench/question.jsonl",
    split="train"
)

for i in tqdm(range(len(mtbench))):
    turns = mtbench[i]["turns"]

    for turn in turns:
        input_text = f"User: {turn}\nAssistant: "

        data = {
            "prompt": input_text,
            "n_predict": 512,
            "stop": "\n"
        }

        requests.post(url, headers=headers, json=data)
