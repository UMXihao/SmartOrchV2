#!/usr/bin/env python3
"""
使用llama.cpp的llama-server评估TextVQA数据集（修复版本）
"""

import os
import json
import requests
import base64
from PIL import Image
import io
import time
from typing import List, Dict, Any
from tqdm import tqdm
import argparse
import numpy as np
import zipfile
import tarfile
from pathlib import Path


class TextVQAEvaluator:
    def __init__(self,
                 server_url: str = "http://localhost:8080",
                 max_tokens: int = 100,
                 temperature: float = 0.2):
        """
        初始化TextVQA评估器
        """
        self.server_url = server_url
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.completion_endpoint = f"{server_url}/v1/completions"
        self.chat_endpoint = f"{server_url}/v1/chat/completions"

        # 测试连接
        self._test_connection()

    def _test_connection(self):
        """测试服务器连接"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ 成功连接到llama-server: {self.server_url}")
            else:
                print(f"⚠️  服务器返回非200状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 无法连接到llama-server: {e}")
            print("请确保已启动llama-server：")
            print("./llama-server -m models/llava.q4_0.gguf --host 0.0.0.0 --port 8080")
            exit(1)

    def _image_to_base64(self, image_path: str) -> str:
        """
        将图像转换为base64编码
        """
        try:
            with Image.open(image_path) as img:
                # 转换为RGB模式
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # 调整大小
                max_size = 512
                if max(img.size) > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

                # 保存到字节流
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG", quality=85)
                img_str = base64.b64encode(buffered.getvalue()).decode()
                return img_str
        except Exception as e:
            print(f"❌ 图像处理失败 {image_path}: {e}")
            return ""

    def query_model(self, prompt: str, image_path: str = None) -> str:
        """
        向模型发送查询
        """
        try:
            # 构建请求数据
            messages = []

            if image_path and os.path.exists(image_path):
                # 处理图像
                image_b64 = self._image_to_base64(image_path)
                if not image_b64:
                    return "图像处理失败"

                content = [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            else:
                content = [{"type": "text", "text": prompt}]

            messages.append({"role": "user", "content": content})

            payload = {
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": False
            }

            # 发送请求
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"❌ 请求失败: {response.status_code}")
                return ""

        except requests.exceptions.Timeout:
            print(f"❌ 请求超时")
            return ""
        except Exception as e:
            print(f"❌ 查询出错: {e}")
            return ""

    def load_textvqa_data(self, data_dir: str = "/home/lili-5090/Sean/SmartOrchV2/models", split: str = "test") -> List[Dict]:
        """
        加载TextVQA数据（手动加载方式）
        """
        data_path = os.path.join(data_dir, f"TextVQA_0.5.1_{split}.json")

        if not os.path.exists(data_path):
            print(f"❌ TextVQA数据文件不存在: {data_path}")
            print("请先下载TextVQA数据：")
            print("1. 访问 https://textvqa.org/dataset")
            print("2. 下载 TextVQA_0.5.1_val.json, TextVQA_0.5.1_train.json")
            print("3. 将文件放入 ./data/textvqa/ 目录")
            return []

        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 提取问题和答案
            questions = data.get('data', [])
            processed_data = []

            for q in questions:
                processed_data.append({
                    "question_id": q.get("question_id", ""),
                    "image_id": q.get("image_id", ""),
                    "question": q.get("question", ""),
                    "answers": q.get("answers", [])
                })

            print(f"✅ 已加载 {len(processed_data)} 个{split}样本")
            return processed_data

        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return []

    def evaluate_single_example(self, example: Dict, images_dir: str) -> Dict:
        """
        评估单个TextVQA样本
        """
        # 构建图像路径
        image_id = example["image_id"]
        image_path = None

        # 尝试多个可能的图像路径
        possible_paths = [
            os.path.join(images_dir, f"{image_id}.jpg"),
            os.path.join(images_dir, f"{image_id}.png"),
            os.path.join(images_dir, f"{image_id}.jpeg"),
            os.path.join(images_dir, "train_images", f"{image_id}.jpg"),
            os.path.join(images_dir, "val_images", f"{image_id}.jpg"),
            os.path.join(images_dir, "test_images", f"{image_id}.jpg"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                image_path = path
                break

        if not image_path:
            print(f"⚠️  图像不存在: {image_id}")
            return None

        # 构建提示词
        question = example["question"]
        prompt = f"""请仔细阅读图像中的文字，然后回答问题。

问题: {question}

请基于图像内容回答，不要添加额外信息。"""

        # 查询模型
        start_time = time.time()
        response = self.query_model(prompt, image_path)
        inference_time = time.time() - start_time

        if not response:
            return None

        # 准备结果
        result = {
            "question_id": example["question_id"],
            "image_id": example["image_id"],
            "question": question,
            "predicted_answer": response,
            "inference_time": inference_time,
            "image_path": image_path
        }

        # 添加参考答案
        if "answers" in example:
            result["reference_answers"] = example["answers"]

        return result

    def evaluate_dataset(self,
                         split: str = "val",
                         max_samples: int = None,
                         output_file: str = "textvqa_results.json") -> None:
        """
        评估整个TextVQA数据集
        """
        print(f"📥 正在加载TextVQA数据 ({split} split)...")

        # 加载数据
        data = self.load_textvqa_data(split=split)

        if not data:
            return

        # 限制样本数
        if max_samples:
            data = data[:max_samples]

        # 获取图像目录
        # images_dir = os.path.join("data", "textvqa", "images")
        images_dir = "/models/test_images"

        if not os.path.exists(images_dir):
            print(f"⚠️  图像目录不存在: {images_dir}")
            print("请先下载TextVQA图像：")
            print("运行: python evaluate_textvqa_fixed.py --download-images")
            return

        print(f"📷 图像目录: {images_dir}")

        # 评估每个样本
        results = []
        failed_samples = []

        for i, example in enumerate(tqdm(data, desc="评估进度")):
            result = self.evaluate_single_example(example, images_dir)

            if result:
                results.append(result)

                # 打印示例
                if (i + 1) % 10 == 0:
                    print(f"\n📊 样本 {i + 1}/{len(data)}:")
                    print(f"   问题: {example['question'][:80]}...")
                    print(f"   预测: {result['predicted_answer'][:80]}...")
                    if "reference_answers" in result:
                        print(f"   参考: {result['reference_answers'][:3]}")
            else:
                failed_samples.append(i)

            # 添加延迟
            time.sleep(0.2)

        # 保存结果
        output_path = os.path.join("results", output_file)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "dataset": "TextVQA",
                    "split": split,
                    "total_samples": len(data),
                    "successful_samples": len(results),
                    "failed_samples": len(failed_samples),
                    "evaluation_date": time.strftime("%Y-%m-%d %H:%M:%S")
                },
                "results": results
            }, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 评估完成！")
        print(f"   总样本: {len(data)}")
        print(f"   成功: {len(results)}")
        print(f"   失败: {len(failed_samples)}")
        print(f"   结果保存至: {output_path}")

        # 计算统计信息
        if results:
            self._calculate_metrics(results)

# def download_textvqa_data():
#     """下载TextVQA数据集"""
#     import urllib.request
#
#     # 创建目录
#     os.makedirs("data/textvqa", exist_ok=True)
#
#     # 数据文件URL
#     data_urls = {
#         "train": "https://dl.fbaipublicfiles.com/textvqa/data/TextVQA_0.5.1_train.json",
#         "val": "https://dl.fbaipublicfiles.com/textvqa/data/TextVQA_0.5.1_val.json",
#         "test": "https://dl.fbaipublicfiles.com/textvqa/data/TextVQA_0.5.1_test.json"
#     }
#
#     print("📥 正在下载TextVQA数据文件...")
#
#     for split, url in data_urls.items():
#         filename = f"TextVQA_0.5.1_{split}.json"
#         filepath = os.path.join("data", "textvqa", filename)
#
#         if not os.path.exists(filepath):
#             print(f"  下载 {filename}...")
#             try:
#                 urllib.request.urlretrieve(url, filepath)
#                 print(f"  ✅ 下载完成: {filename}")
#             except Exception as e:
#                 print(f"  ❌ 下载失败: {e}")
#         else:
#             print(f"  ✅ 文件已存在: {filename}")
#
#
# def download_textvqa_images():
#     """下载TextVQA图像"""
#     import urllib.request
#
#     print("📥 正在下载TextVQA图像...")
#     print("⚠️  注意：图像文件较大，请确保有足够磁盘空间")
#
#     # 图像URL
#     image_urls = {
#         "train_val": "https://dl.fbaipublicfiles.com/textvqa/images/train_val_images.zip",
#         "test": "https://dl.fbaipublicfiles.com/textvqa/images/test_images.zip"
#     }
#
#     images_dir = "data/textvqa/images"
#     os.makedirs(images_dir, exist_ok=True)
#
#     for name, url in image_urls.items():
#         zip_path = os.path.join(images_dir, f"{name}.zip")
#
#         if not os.path.exists(zip_path):
#             print(f"  下载 {name} 图像...")
#             try:
#                 # 显示进度
#                 def reporthook(count, block_size, total_size):
#                     percent = int(count * block_size * 100 / total_size)
#                     print(f"    进度: {percent}%", end='\r')
#
#                 urllib.request.urlretrieve(url, zip_path, reporthook)
#                 print(f"\n  ✅ 下载完成: {name}")
#
#                 # 解压
#                 print(f"  解压 {name}...")
#                 with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#                     zip_ref.extractall(images_dir)
#                 print(f"  ✅ 解压完成")
#
#                 # 删除zip文件
#                 os.remove(zip_path)
#
#             except Exception as e:
#                 print(f"  ❌ 下载失败: {e}")
#         else:
#             print(f"  ✅ 图像已存在: {name}")


def main():
    parser = argparse.ArgumentParser(description="使用llama-server评估TextVQA")
    parser.add_argument("--server", default="http://localhost:8080", help="llama-server地址")

    parser.add_argument("--split", default="test", choices=["train", "val", "test"], help="数据集划分")
    parser.add_argument("--max-samples", type=int, default=50, help="最大评估样本数")
    parser.add_argument("--output", default="textvqa_results.json", help="输出文件名")
    # parser.add_argument("--download-data", action="store_true", help="下载文本数据")
    # parser.add_argument("--download-images", action="store_true", help="下载图像数据")

    args = parser.parse_args()

    # 下载数据
    # if args.download_data:
    #     download_textvqa_data()
    #     return
    #
    # if args.download_images:
    #     download_textvqa_images()
    #     return

    # 创建评估器
    evaluator = TextVQAEvaluator(
        server_url=args.server,
        max_tokens=150,
        temperature=0.1
    )

    # 运行评估
    evaluator.evaluate_dataset(
        split=args.split,
        max_samples=args.max_samples,
        output_file=args.output
    )


if __name__ == "__main__":
    main()

