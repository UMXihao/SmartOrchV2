"""
start llama.cpp server at ~/SmartOrchV2
./build/bin/llama-server -m ${model_path}

using llama-server to finish bench mark
"""

import requests
import time
from tqdm import tqdm
from datasets import load_dataset
import evaluate

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

human_eval = load_dataset("bigcode/humanevalpack", "python")["test"]

predictions = []
references = []

# modify 100

start_time = time.time()
for i in tqdm(range(100)):
    question = human_eval[i]["prompt"]

    # 构造输入文本
    input_text = f"{question}"
    data = {"prompt": input_text, "n_predict": 128, "stop": "\n"}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
