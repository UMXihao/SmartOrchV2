# scripts/build_mtbench_prompts.py

import argparse
import csv
import json
import os
from typing import List, Dict, Any

from datasets import load_dataset


MTBENCH_EVAL_URL = (
    "https://raw.githubusercontent.com/lm-sys/FastChat/main/"
    "fastchat/llm_judge/data/mt_bench/question.jsonl"
)


def clean_text(text: str) -> str:
    return str(text).replace("\n", " ").strip()


def build_prompt(turns: List[str], prompt_style: str = "chat") -> str:
    """
    Build a prompt for MT-Bench.

    MT-Bench contains multi-turn questions:
      - turns[0]: first user question
      - turns[1]: optional follow-up question

    For most single-turn inference pipelines, you can use only turns[0].
    For multi-turn evaluation, use prompt_style="chat" to keep all turns.
    """
    turns = [clean_text(t) for t in turns if str(t).strip()]

    if prompt_style == "simple":
        return turns[0] if turns else ""

    if prompt_style == "first_turn":
        return (
            "You are a helpful assistant.\n\n"
            f"User: {turns[0] if turns else ''}\n"
            "Assistant:"
        )

    if prompt_style == "chat":
        parts = ["You are a helpful assistant."]
        for i, turn in enumerate(turns, start=1):
            parts.append(f"\nUser turn {i}:\n{turn}\n\nAssistant:")
        return "\n".join(parts)

    raise ValueError(f"Unsupported prompt_style: {prompt_style}")


def write_jsonl(rows: List[Dict[str, Any]], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        for item in rows:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def write_csv(rows: List[Dict[str, Any]], out_path: str) -> None:
    fieldnames = [
        "id",
        "question_id",
        "category",
        "turn_id",
        "num_turns",
        "instruction",
        "prompt",
        "turns_json",
    ]

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in rows:
            writer.writerow(item)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--out",
        required=True,
        help="Output file path. Supports .jsonl or .csv."
    )

    parser.add_argument(
        "--max",
        type=int,
        default=-1,
        help="Max number of questions to export. -1 means all."
    )

    parser.add_argument(
        "--prompt_style",
        choices=["simple", "first_turn", "chat"],
        default="chat",
        help=(
            "Prompt format. "
            "simple: raw first turn only; "
            "first_turn: first turn with User/Assistant template; "
            "chat: preserve all MT-Bench turns."
        )
    )

    parser.add_argument(
        "--one_row_per_turn",
        action="store_true",
        help=(
            "Export each MT-Bench turn as a separate row. "
            "By default, each MT-Bench question is exported as one row."
        )
    )

    args = parser.parse_args()

    # Load MT-Bench questions from the official FastChat question.jsonl file.
    ds = load_dataset(
        "json",
        data_files=MTBENCH_EVAL_URL,
        split="train",
    )

    rows = []
    n = 0

    for row in ds:
        question_id = row.get("question_id", str(n))
        category = row.get("category", "")
        turns = row.get("turns", [])

        if not isinstance(turns, list):
            turns = [str(turns)]

        if args.one_row_per_turn:
            for turn_idx, turn in enumerate(turns):
                instruction = clean_text(turn)
                prompt = build_prompt([instruction], prompt_style=args.prompt_style)

                rows.append({
                    "id": f"{question_id}_{turn_idx}",
                    "question_id": question_id,
                    "category": category,
                    "turn_id": turn_idx,
                    "num_turns": len(turns),
                    "instruction": instruction,
                    "prompt": prompt,
                    "turns_json": json.dumps(turns, ensure_ascii=False),
                })
        else:
            prompt = build_prompt(turns, prompt_style=args.prompt_style)
            instruction = clean_text(turns[0]) if turns else ""

            rows.append({
                "id": str(question_id),
                "question_id": question_id,
                "category": category,
                "turn_id": "",
                "num_turns": len(turns),
                "instruction": instruction,
                "prompt": prompt,
                "turns_json": json.dumps(turns, ensure_ascii=False),
            })

        n += 1
        if args.max > 0 and n >= args.max:
            break

    ext = os.path.splitext(args.out)[1].lower()

    if ext == ".csv":
        write_csv(rows, args.out)
    elif ext == ".jsonl":
        write_jsonl(rows, args.out)
    else:
        raise ValueError("Unsupported output format. Please use .csv or .jsonl")

    print(f"Exported {len(rows)} prompts to {args.out}")


if __name__ == "__main__":
    main()
