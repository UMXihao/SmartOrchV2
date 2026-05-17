# scripts/build_squad_prompts.py

import argparse
import json
from datasets import load_dataset


def build_prompt(context: str, question: str) -> str:
    context = context.replace("\n", " ").strip()
    question = question.replace("\n", " ").strip()

    return (
        "You are a question answering assistant.\n"
        "Answer the question based only on the given context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        "Answer:"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        default="squad",
        help="Hugging Face dataset name, e.g. squad or squad_v2"
    )

    parser.add_argument(
        "--split",
        default="train",
        help="Dataset split, e.g. train or validation"
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output jsonl file path"
    )

    parser.add_argument(
        "--max",
        type=int,
        default=-1,
        help="Max number of prompts to export. -1 means all."
    )

    parser.add_argument(
        "--streaming",
        action="store_true",
        help="Use Hugging Face streaming mode"
    )

    args = parser.parse_args()

    ds = load_dataset(
        args.dataset,
        split=args.split,
        streaming=args.streaming
    )

    n = 0

    with open(args.out, "w", encoding="utf-8") as f:
        for row in ds:
            context = row["context"]
            question = row["question"]

            prompt = build_prompt(context, question)

            item = {
                "id": row.get("id", str(n)),
                "title": row.get("title", ""),
                "prompt": prompt,
            }

            f.write(json.dumps(item, ensure_ascii=False) + "\n")

            n += 1
            if args.max > 0 and n >= args.max:
                break

    print(f"Exported {n} prompts to {args.out}")


if __name__ == "__main__":
    main()

'''
python squad_prompts_build.py \
  --dataset squad \
  --split validation \
  --out squad_validation_test.jsonl \
  --max 100

# default jsonl path attn-head/squad_validation_test.jsonl

./build/bin/llama-head-importance \
  -m ../llama.cpp/models/deepseek-v2-lite-chat.gguf \
  -c 4096 \
  -ngl 0
'''
