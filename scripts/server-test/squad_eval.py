"""
start llama.cpp server
build/bin/llama-server -m ${model_path}

using llama-server to finish bench mark
"""

import requests
import time
from tqdm import tqdm
from datasets import load_dataset
import evaluate

url = "http://127.0.0.1:8080/completion"
# url = "http://127.0.0.1:8080/v1/chat/completions"
headers = {"Content-Type": "application/json"}
# data = {
#     "model": "meta-llama-3-8B-Q4",
#     "messages": [{"role": "user", "content": "Hello, how are you?"}],
#     "max_tokens": 128
# }

squad_val = load_dataset("squad", split="validation")

predictions = []
references = []

start_time = time.time()
for i in tqdm(range(100)):
    # for i in tqdm(range(len(dataset))):
    context = squad_val[i]["context"]
    question = squad_val[i]["question"]
    answers = squad_val[i]["answers"]
    question_id = squad_val[i]["id"]

    # 构造输入文本
    input_text = f"Context: {context}\nQuestion: {question}\nAnswer: "
    data = {"prompt": input_text, "n_predict": 128, "stop": "\n"}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    reference = {'answers': answers, 'id': question_id}
    prediction = {'prediction_text': response.json().get("content"), 'id': question_id}

    references.append(reference)
    predictions.append(prediction)

result = evaluate.load("squad").compute(predictions=predictions, references=references)
print(result)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"requests: {elapsed_time:.2f} seconds")

'''
./build/bin/llama-server -m /data/DeepSeek-Coder-V2-Lite-Instruct-IQ2_XS.gguf -ngl 33

squad-validation:
{'exact_match': 1.4001892147587511, 'f1': 9.460719074946544}
requests: 6696.57 seconds

{'exact_match': 3.0, 'f1': 10.137294917520338}
requests: 2877.42 seconds
'''