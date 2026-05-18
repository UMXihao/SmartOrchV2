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

# url = "http://127.0.0.1:8080/completion"
url = "http://127.0.0.1:8080/chat/completions"
headers = {"Content-Type": "application/json"}

POS = "POSITIVE"
NEG = "NEGATIVE"
VALID_LABELS = {POS, NEG}
RANDOM_SEED = 42

ds = load_dataset("imdb")
dataset = ds["test"]

SYSTEM_PROMPT = (
    "You are a sentiment classifier for movie reviews.\n"
    "Classify the given review as POSITIVE or NEGATIVE.\n"
    "Answer with exactly one word: POSITIVE or NEGATIVE.\n"
)

predictions = []
references = []

def normalize_pred(text: str):
    if text is None:
        return None
    s = text.strip().upper()

    if POS in s:
        return POS
    if NEG in s:
        return NEG
    return None


n_ok = 0
n_fail = 0

start_time = time.time()
for i in tqdm(range(100)):
    # for i in tqdm(range(len(dataset))):

    ex = dataset[i]
    user_prompt = ex["text"]
    label = ex["label"]  # 0=negative, 1=positive
    gt = POS if label == 1 else NEG

    # print("Label: ", gt)
    # print("input: ", user_prompt)
    data = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "n_predict": 128, "stop": "\n"
    }

    response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#
#
#     data = response.json()
#     output = data["choices"][0]["message"]["content"]
#     # print("output: ", data)
#     # print("output: ", output)
#     prediction = normalize_pred(output)
#     # print("prediction: ", prediction)
#
#     ok = (prediction == gt)
#     if prediction is None:
#         n_fail += 1
#     elif ok:
#         n_ok += 1
#
#
# result = n_ok/1000
# print("acc: ", result)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"requests: {elapsed_time:.2f} seconds")

'''
Label:  NEGATIVE
input:  I love sci-fi and am willing to put up with a lot. Sci-fi movies/TV are usually underfunded, under-appreciated and misunderstood. I tried to like this, I really did, but it is to good TV sci-fi as Babylon 5 is to Star Trek (the original). Silly prosthetics, cheap cardboard sets, stilted dialogues, CG that doesn't match the background, and painfully one-dimensional characters cannot be overcome with a 'sci-fi' setting. (I'm sure there are those of you out there who think Babylon 5 is good sci-fi TV. It's not. It's clichéd and uninspiring.) While US viewers might like emotion and character development, sci-fi is a genre that does not take itself seriously (cf. Star Trek). It may treat important issues, yet not as a serious philosophy. It's really difficult to care about the characters here as they are not simply foolish, just missing a spark of life. Their actions and reactions are wooden and predictable, often painful to watch. The makers of Earth KNOW it's rubbish as they have to always say "Gene Roddenberry's Earth..." otherwise people would not continue watching. Roddenberry's ashes must be turning in their orbit as this dull, cheap, poorly edited (watching it without advert breaks really brings this home) trudging Trabant of a show lumbers into space. Spoiler. So, kill off a main character. And then bring him back as another actor. Jeeez! Dallas all over again.
data:  {'choices': [{'finish_reason': 'stop', 'index': 0, 'message': {'role': 'assistant', 'content': ' The review is negative.'}}], 'created': 1767003682, 'model': 'gpt-3.5-turbo', 'system_fingerprint': 'b7038-a422085a', 'object': 'chat.completion', 'usage': {'completion_tokens': 6, 'prompt_tokens': 374, 'total_tokens': 380}, 'id': 'chatcmpl-6n43aKQe8lBY0o100JZn0mN08XSw3KQS', 'timings': {'cache_n': 373, 'prompt_n': 1, 'prompt_ms': 278.682, 'prompt_per_token_ms': 278.682, 'prompt_per_second': 3.5883193030048584, 'predicted_n': 6, 'predicted_ms': 1348.89, 'predicted_per_token_ms': 224.81500000000003, 'predicted_per_second': 4.448101772568556}}
output:   The review is negative.
prediction:  NEGATIVE

acc:  0.18
requests: 8021.31 seconds
'''
