import requests
from tqdm import tqdm
from datasets import load_dataset
import evaluate
import time

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

# 加载 CNN/DailyMail 验证集
summarization_val = load_dataset(
    "cnn_dailymail",
    "3.0.0",
    split="validation"
)

# 加载 ROUGE 评测指标
rouge = evaluate.load("rouge")

predictions = []
references = []

# 可先小规模测试，确认流程无误
max_samples = 10
# max_samples = len(summarization_val)

total_time = 0

for i in tqdm(range(max_samples)):
    article = summarization_val[i]["article"]
    reference_summary = summarization_val[i]["highlights"]

    input_text = (
        "Please summarize the following article.\n\n"
        f"Article: {article}\n\n"
        "Summary:"
    )

    data = {
        "prompt": input_text,
        "n_predict": 1024,
        "stop": ["\n"]
    }

    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()

        predict = response.json().get("content", "")
        predict = predict.strip()

    except Exception as e:
        print(f"\n样本 {i} 推理失败: {e}")
        predict = ""

    end_time = time.time()
    total_time += end_time - start_time

    predictions.append(predict)
    references.append(reference_summary.strip())

    # 计算 ROUGE
    results = rouge.compute(
        predictions=predictions,
        references=references,
        use_stemmer=True
    )
    predictions = []
    references = []
    print("\n===== 推理精度评测结果 =====")
    for k, v in results.items():
        print(f"{k}: {v:.4f}")
