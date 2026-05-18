import requests
from tqdm import tqdm
from datasets import load_dataset

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

# 加载文本摘要数据集
# CNN/DailyMail 是常用的英文摘要数据集
summarization_val = load_dataset(
    "cnn_dailymail",
    "3.0.0",
    split="validation"
)

for i in tqdm(range(100)):
    # for i in tqdm(range(len(summarization_val))):
    article = summarization_val[i]["article"]

    # 构造摘要任务输入
    input_text = (
        "Please summarize the following article.\n\n"
        f"Article: {article}\n\n"
        "Summary:"
    )

    data = {
        "prompt": input_text,
        "n_predict": 128,
        "stop": "\n\n"
    }

    requests.post(url, headers=headers, json=data)
