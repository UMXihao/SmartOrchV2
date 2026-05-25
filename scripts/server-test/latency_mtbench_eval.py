import requests
from tqdm import tqdm
from datasets import load_dataset
import evaluate
import numpy as np

def trimmed_mean_np(arr):
    arr = np.asarray(arr)

    if arr.size <= 6:
        raise ValueError("数组长度必须大于 6")

    sorted_arr = np.sort(arr)
    trimmed = sorted_arr[3:-3]

    return np.mean(trimmed)

def percentile(data, percentile):
    return float(np.percentile(data, percentile, method="linear"))

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

mtbench = load_dataset(
    "json",
    data_files="https://huggingface.co/spaces/lmsys/mt-bench/raw/main/data/mt_bench/question.jsonl",
    split="train"
)

predictions = []
references = []
prefill = []
token_num = []
decode = []

# for i in tqdm(range(len(mtbench))):
for i in tqdm(range(10)):
    turns = mtbench[i]["turns"]

    for turn in turns:
        input_text = f"User: {turn}\nAssistant: "

        data = {
            "prompt": input_text,
            "n_predict": 10,
            "stop": "\n"
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        predict = response.json().get("content")

        # reference = {'answers': answers, 'id': question_id}
        # prediction = {'prediction_text': predict, 'id': question_id}
        prompt_ms = response.json().get("timings").get("prompt_ms")
        prompt_per_second = response.json().get("timings").get("prompt_per_second")
        predicted_per_token_ms = response.json().get("timings").get("predicted_per_token_ms")
        # print("TTFT: ", prompt_ms, " TPOT: ", predicted_per_token_ms)
        prefill.append(prompt_ms)
        token_num.append(prompt_per_second)
        decode.append(predicted_per_token_ms)

        # references.append(reference)
        # predictions.append(prediction)

    # result = evaluate.load("squad").compute(predictions=predictions, references=references)
    # print(result)

print("==========PREFILL============")
print("MEAN = ", trimmed_mean_np(prefill), " ms")
print("P50 = ", percentile(prefill, 50), " ms")
print("P90 = ", percentile(prefill, 90), " ms")
print("P99 = ", percentile(prefill, 99), " ms")
print("==========PREFILL TOKEN NUMBER============")
print("MEAN = ", trimmed_mean_np(token_num))
print("P50 = ", percentile(token_num, 50))
print("P90 = ", percentile(token_num, 90))
print("P99 = ", percentile(token_num, 99))
print("==========DECODE============")
print("MEAN = ", trimmed_mean_np(decode), " ms")
print("P50 = ", percentile(decode, 50), " ms")
print("P90 = ", percentile(decode, 90), " ms")
print("P99 = ", percentile(decode, 99), " ms")
print(
    f"{trimmed_mean_np(prefill):.2f},"
    f"{np.percentile(prefill, 50):.2f},"
    f"{np.percentile(prefill, 90):.2f},"
    f"{np.percentile(prefill, 99):.2f},"
    f"{trimmed_mean_np(token_num):.2f},"
    f"{np.percentile(token_num, 50):.2f},"
    f"{np.percentile(token_num, 90):.2f},"
    f"{np.percentile(token_num, 99):.2f},"
    f"{trimmed_mean_np(decode):.2f},"
    f"{np.percentile(decode, 50):.2f},"
    f"{np.percentile(decode, 90):.2f},"
    f"{np.percentile(decode, 99):.2f}"
)
