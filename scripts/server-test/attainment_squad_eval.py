import requests
from tqdm import tqdm
from datasets import load_dataset
import evaluate

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

squad_val = load_dataset("squad", split="validation")

predictions = []
references = []

count = 0
for i in tqdm(range(1000)):
#for i in tqdm(range(len(squad_val))):
    context = squad_val[i]["context"]
    question = squad_val[i]["question"]
    answers = squad_val[i]["answers"]
    question_id = squad_val[i]["id"]

    # 构造输入文本
    input_text = f"Context: {context}\nQuestion: {question}\nAnswer: "
    data = {"prompt": input_text, "n_predict": 128, "stop": "\n"}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    predict = response.json().get("content")
    reference = {'answers': answers, 'id': question_id}
    prediction = {'prediction_text': predict, 'id': question_id}

    references.append(reference)
    predictions.append(prediction)

    result = evaluate.load("squad").compute(predictions=predictions, references=references)
    predictions = []
    references = []
    print(result.get('f1'))
    if result.get('f1') > 19.09:
        count = count + 1
    # print(result.get('f1'))

with open("count.txt", "w", encoding="utf-8") as f:
    f.write(str(count))
