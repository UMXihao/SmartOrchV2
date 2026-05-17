# scripts/build_alpaca_eval_prompts.py

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Any

from datasets import load_dataset


def clean_text(text: Any) -> str:
    """Normalize text fields to one-line-safe strings for CSV/JSONL export."""
    if text is None:
        return ""
    return str(text).replace("\r", " ").replace("\n", " ").strip()


def build_prompt(instruction: str, style: str = "alpaca") -> str:
    """
    Build an inference prompt from AlpacaEval's instruction field.

    Important: AlpacaEval is an instruction-following eval set. The reference/baseline
    output should NOT be placed in the prompt when generating model responses.
    """
    instruction = clean_text(instruction)

    if style == "simple":
        return instruction

    if style == "chat":
        return (
            "You are a helpful assistant.\n\n"
            f"User: {instruction}\n"
            "Assistant:"
        )

    # Default Alpaca-style prompt.
    return (
        "Below is an instruction that describes a task. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n"
        f"{instruction}\n\n"
        "### Response:"
    )


def write_csv_row(writer: csv.DictWriter, item: Dict[str, Any]) -> None:
    writer.writerow({k: clean_text(v) for k, v in item.items()})


def main():
    parser = argparse.ArgumentParser(
        description="Export AlpacaEval instructions/prompts to CSV or JSONL."
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output file path, e.g. alpaca_eval.csv or alpaca_eval.jsonl",
    )

    parser.add_argument(
        "--format",
        choices=["csv", "jsonl"],
        default="jsonl",
        help="Output format. If omitted, inferred from --out suffix.",
    )

    parser.add_argument(
        "--max",
        type=int,
        default=-1,
        help="Max number of examples to export. -1 means all.",
    )

    parser.add_argument(
        "--prompt_style",
        choices=["alpaca", "simple", "chat"],
        default="alpaca",
        help="Prompt template style used for the exported prompt column.",
    )

    args = parser.parse_args()

    out_path = Path(args.out)
    out_format = args.format or out_path.suffix.lstrip(".").lower()
    if out_format not in {"csv", "jsonl"}:
        raise ValueError("Output format must be csv or jsonl. Use --format if needed.")

    ALPACA_EVAL_URL = (
        "https://huggingface.co/datasets/tatsu-lab/alpaca_eval/resolve/main/alpaca_eval.json"
    )

    ds = load_dataset(
        "json",
        data_files=ALPACA_EVAL_URL,
        split="train",
    )

    fieldnames = [
        "id",
        "instruction",
        "prompt",
        "reference_output",
        "generator",
        "dataset",
    ]

    n = 0
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        if out_format == "csv":
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        else:
            writer = None

        for row in ds:
            instruction = row.get("instruction", "")
            prompt = build_prompt(instruction, style=args.prompt_style)

            item = {
                "id": row.get("id", str(n)),
                "instruction": instruction,
                "prompt": prompt,
                # Keep the dataset-provided output as a separate reference/baseline column.
                # Do not include this field in the prompt for model generation.
                "reference_output": row.get("output", ""),
                "generator": row.get("generator", ""),
                "dataset": row.get("dataset", ""),
            }

            if out_format == "csv":
                write_csv_row(writer, item)
            else:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

            n += 1
            if args.max > 0 and n >= args.max:
                break

    print(f"Exported {n} examples to {out_path}")


if __name__ == "__main__":
    main()

'''
    python alpaca_prompts_build.py \
      --out squad_validation_test.jsonl \
      --max 100
'''
