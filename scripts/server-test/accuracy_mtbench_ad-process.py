import json
import time
import uuid
import requests
from tqdm import tqdm
from datasets import load_dataset

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

MODEL_ID = "my-local-model"
ANSWER_FILE = f"{MODEL_ID}_mtbench_answer.jsonl"

mtbench = load_dataset(
    "json",
    data_files="https://huggingface.co/spaces/lmsys/mt-bench/raw/main/data/mt_bench/question.jsonl",
    split="train"
)

def build_prompt(messages):
    """
    把多轮对话历史拼成 completion 模型可用的 prompt。
    如果你的模型有自己的 chat template，需要在这里替换。
    """
    prompt = (
        "A chat between a curious user and an artificial intelligence assistant. "
        "The assistant gives helpful, detailed, and polite answers.\n\n"
    )

    for msg in messages:
        if msg["role"] == "user":
            prompt += f"User: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"Assistant: {msg['content']}\n"

    prompt += "Assistant:"
    return prompt


def call_model(prompt, n_predict=10):
    data = {
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": 0.7,
        "top_p": 0.95,
        "stop": [
            "\nUser:",
            "\n\nUser:",
            "</s>"
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=300
    )
    response.raise_for_status()

    return response.json().get("content", "").strip()


with open(ANSWER_FILE, "w", encoding="utf-8") as fout:
    # 先跑 10 条验证流程
    for i in tqdm(range(10)):
    # 跑完整 MT-Bench
    # for i in tqdm(range(len(mtbench))):
        item = mtbench[i]
        question_id = item["question_id"]
        category = item.get("category", "")
        turns = item["turns"]

        messages = []
        answer_turns = []

        for turn in turns:
            messages.append({
                "role": "user",
                "content": turn
            })

            prompt = build_prompt(messages)
            answer = call_model(prompt, n_predict=1024)

            answer_turns.append(answer)

            messages.append({
                "role": "assistant",
                "content": answer
            })

        record = {
            "question_id": question_id,
            "answer_id": str(uuid.uuid4()),
            "model_id": MODEL_ID,
            "choices": [
                {
                    "index": 0,
                    "turns": answer_turns
                }
            ],
            "tstamp": time.time()
        }

        fout.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"MT-Bench answers saved to: {ANSWER_FILE}")
