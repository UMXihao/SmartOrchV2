import os
import torch
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM


def collect_prefill_attentions(
    model_name_or_path: str,
    text: str,
    device: str = "cpu",
    dtype: torch.dtype = torch.float16,
):
    """
    采集 prefill 阶段的 attention。

    返回:
        tokens: List[str]
        attentions: tuple of length num_layers
            每个元素 shape = [batch, num_heads, seq_len, seq_len]
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        dtype=dtype,
        trust_remote_code=True,
    ).to(device)

    model.set_attn_implementation("eager")
    model.eval()

    inputs = tokenizer(text, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(
            **inputs,
            output_attentions=True,
            use_cache=False,   # 明确只看 prefill，一次性全序列前向
            return_dict=True,
        )

    input_ids = inputs["input_ids"][0]
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # tuple[num_layers]，每层 [batch, heads, q_len, k_len]
    attentions = outputs.attentions

    return tokens, attentions


def plot_attention_heatmap(
    tokens,
    attentions,
    layer_idx: int,
    head_idx: int,
    save_path: str = None,
    max_labels: int = 80,
    figsize=(10, 8),
):
    """
    绘制某一层某个 head 的 attention 热力图。
    """
    attn = attentions[layer_idx][0, head_idx].detach().float().cpu()  # [seq_len, seq_len]
    seq_len = attn.shape[0]

    plt.figure(figsize=figsize)
    # plt.imshow(attn.numpy(), aspect="auto", origin="lower")
    # Greens   Blues   Purples
    plt.imshow(attn.numpy(), aspect="auto", origin="lower", cmap="Purples")
    plt.colorbar(label="attention weight")

    # token 太多时，避免坐标轴爆炸
    if seq_len <= max_labels:
        plt.xticks(range(seq_len), tokens, rotation=90, fontsize=8)
        plt.yticks(range(seq_len), tokens, fontsize=8)
    else:
        step = max(1, seq_len // max_labels)
        idxs = list(range(0, seq_len, step))
        show_tokens = [tokens[i] for i in idxs]
        plt.xticks(idxs, show_tokens, rotation=90, fontsize=8)
        plt.yticks(idxs, show_tokens, fontsize=8)

    plt.xlabel("Key positions")
    plt.ylabel("Query positions")
    plt.title(f"Prefill Attention Heatmap | layer={layer_idx}, head={head_idx}")
    plt.tight_layout()

    plt.savefig(save_path, format="pdf", bbox_inches="tight")


if __name__ == "__main__":
    model_name = "/data/DeepSeek-Coder-V2-Lite-Base/"   # 改成你的模型
    # model_name = "/data/Qwen2.5-1.5B/"
    # text = (
    #     "Question: In which city is the Eiffel Tower located?\n"
    #     "Answer:"
    # )

    # text = (
    #     "Write a Python function to check whether a number is prime. The function should return True if it is prime, otherwise False."
    #     "Write a Python function to check whether a number is prime. The function should return True if it is prime, otherwise False."
    # )

    text = (
            '''The internet, a global network connecting billions of devices, has profoundly reshaped nearly every aspect of modern life. Its origins, however, are surprisingly modest.  The story begins in the Cold War era, with the U.S. Department of Defense’s Advanced Research Projects Agency (ARPA).  In 1969, ARPA created ARPANET, a project designed to enable researchers to share computer resources. This initial network connected just four universities: UCLA, Stanford Research Institute, UC Santa Barbara, and the University of Utah. The primary goal wasn’t about cat videos or social media – it was about creating a decentralized communication system that could withstand a potential Soviet attack.  If one part of the network went down, others would remain operational.

Throughout the 1970s, ARPANET evolved, with the development of crucial protocols like TCP/IP (Transmission Control Protocol/Internet Protocol), which became the standard for communication over the network.  Email also emerged as a key application, fundamentally changing how people communicated professionally and personally.  However, access remained largely limited to academic and governmental institutions.

The 1980s saw the transition from ARPANET to the modern internet.  The National Science Foundation (NSF) played a crucial role, establishing NSFNET, a high-speed network connecting supercomputer centers across the United States. This significantly expanded network capacity and accessibility.  Crucially, NSFNET lifted restrictions on commercial traffic, paving the way for the internet’s commercialization.

The invention of the World Wide Web in 1989 by Tim Berners-Lee at CERN, the European Organization for Nuclear Research, was a watershed moment. Berners-Lee created the three fundamental technologies that underpin the Web: HTML (HyperText Markup Language), URL (Uniform Resource Locator), and HTTP (Hypertext Transfer Protocol). These allowed for the creation of interconnected documents and easily navigable information. The first web browser, WorldWideWeb (later renamed Nexus), was also developed.

The 1990s witnessed the explosive growth of the internet, fueled by the release of user-friendly browsers like Mosaic and Netscape Navigator.  The dot-com boom saw a surge of investment in internet-based companies, although many ultimately failed.  Despite the bubble burst, the underlying infrastructure and user base continued to expand rapidly.

Today, the internet is an integral part of global society. It facilitates communication, commerce, education, entertainment, and countless other activities.  Social media platforms connect billions of people worldwide, while e-commerce has revolutionized retail. The rise of mobile devices and wireless internet access has further extended the internet’s reach, making it accessible to an unprecedented number of people.

However, the internet also presents significant challenges. Concerns about privacy, security, misinformation, and digital inequality remain pressing issues. The future of the internet will likely involve ongoing debates about net neutrality, data governance, and the ethical implications of artificial intelligence.  Nevertheless, the internet's impact on humanity is undeniable and continues to unfold.'''

    )
    tokens, attentions = collect_prefill_attentions(
        model_name_or_path=model_name,
        text=text,
        device="cpu",
        dtype=torch.float32,

        # device="cuda" if torch.cuda.is_available() else "cpu",
        # dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )

    # print(f"num_layers = {len(attentions)}")
    print(f"attn shape of layer0 = {attentions[0].shape}")  # [batch, heads, seq, seq]

    # 画第0层第0个head
    plot_attention_heatmap(
        tokens=tokens,
        attentions=attentions,
        layer_idx=0,
        head_idx=0,
        save_path="outputs/Summ.pdf",
    )
