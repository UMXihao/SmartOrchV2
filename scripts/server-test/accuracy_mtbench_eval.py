import json
import re
import requests
from tqdm import tqdm
from datasets import load_dataset

ANSWER_FILE = "my-local-model_mtbench_answer.jsonl"

judge_url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

mtbench = load_dataset(
    "json",
    data_files="https://huggingface.co/spaces/lmsys/mt-bench/raw/main/data/mt_bench/question.jsonl",
    split="train"
)

question_map = {
    item["question_id"]: item
    for item in mtbench
}


def build_single_turn_judge_prompt(question, answer):
    return f"""
[Instruction]
Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below.

Your evaluation should consider factors such as:
- helpfulness
- relevance
- accuracy
- depth
- creativity
- level of detail

Begin your evaluation by providing a short explanation.
Be as objective as possible.

After providing your explanation, rate the response on a scale of 1 to 10 by strictly following this format:
Rating: [[rating]]

[Question]
{question}

[The Start of Assistant's Answer]
{answer}
[The End of Assistant's Answer]
""".strip()


def build_multi_turn_judge_prompt(question_1, answer_1, question_2, answer_2):
    return f"""
[Instruction]
Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant in the following multi-turn conversation.

Your evaluation should focus on the assistant's answer to the second user question.
Your evaluation should consider:
- helpfulness
- relevance
- accuracy
- depth
- creativity
- level of detail

Begin your evaluation by providing a short explanation.
Be as objective as possible.

After providing your explanation, rate the response on a scale of 1 to 10 by strictly following this format:
Rating: [[rating]]

<|The Start of Assistant A's Conversation with User|>

### User:
{question_1}

### Assistant A:
{answer_1}

### User:
{question_2}

### Assistant A:
{answer_2}

<|The End of Assistant A's Conversation with User|>
""".strip()


def call_judge(prompt):
    data = {
        "prompt": prompt,
        "n_predict": 512,
        "temperature": 0.0,
        "stop": ["</s>"]
    }

    response = requests.post(
        judge_url,
        headers=headers,
        json=data,
        timeout=300
    )
    response.raise_for_status()

    return response.json().get("content", "").strip()


def parse_score(judge_output):
    """
    从 judge 输出里解析 [[8]]、Rating: [[8]]、[[8.5]] 这类分数。
    """
    match = re.search(r"\[\[\s*(\d+(?:\.\d+)?)\s*\]\]", judge_output)
    if not match:
        return None

    score = float(match.group(1))

    if score < 1 or score > 10:
        return None

    return score


scores = []
details = []

with open(ANSWER_FILE, "r", encoding="utf-8") as fin:
    lines = fin.readlines()

for line in tqdm(lines):
    record = json.loads(line)

    question_id = record["question_id"]
    model_id = record["model_id"]
    answers = record["choices"][0]["turns"]

    item = question_map[question_id]
    questions = item["turns"]
    category = item.get("category", "")

    # 第 1 轮评分
    prompt_1 = build_single_turn_judge_prompt(
        question=questions[0],
        answer=answers[0]
    )

    judge_output_1 = call_judge(prompt_1)
    score_1 = parse_score(judge_output_1)

    details.append({
        "question_id": question_id,
        "category": category,
        "turn": 1,
        "score": score_1,
        "judge_output": judge_output_1
    })

    if score_1 is not None:
        scores.append(score_1)

    # 第 2 轮评分
    if len(questions) >= 2 and len(answers) >= 2:
        prompt_2 = build_multi_turn_judge_prompt(
            question_1=questions[0],
            answer_1=answers[0],
            question_2=questions[1],
            answer_2=answers[1]
        )

        judge_output_2 = call_judge(prompt_2)
        score_2 = parse_score(judge_output_2)

        details.append({
            "question_id": question_id,
            "category": category,
            "turn": 2,
            "score": score_2,
            "judge_output": judge_output_2
        })

        if score_2 is not None:
            scores.append(score_2)


avg_score = sum(scores) / len(scores) if scores else 0.0

print("\n===== MT-Bench Evaluation Result =====")
print(f"Evaluated model: {model_id}")
print(f"Valid judged turns: {len(scores)}")
print(f"Average MT-Bench score: {avg_score:.4f} / 10")

# 保存详细评分结果
with open("mtbench_judge_details.jsonl", "w", encoding="utf-8") as fout:
    for d in details:
        fout.write(json.dumps(d, ensure_ascii=False) + "\n")

print("Judge details saved to: mtbench_judge_details.jsonl")
