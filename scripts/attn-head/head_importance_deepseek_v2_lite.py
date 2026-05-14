import argparse
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


def build_chat_inputs(tokenizer, prompt):
    messages = [{"role": "user", "content": prompt}]

    # 新版 transformers 支持 return_dict=True
    try:
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )
        return dict(inputs)
    except TypeError:
        # 兼容旧版 tokenizer
        input_ids = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
        )
        return {
            "input_ids": input_ids,
            "attention_mask": torch.ones_like(input_ids),
        }


def get_decoder_layers(model):
    if hasattr(model, "model") and hasattr(model.model, "layers"):
        return model.model.layers
    raise RuntimeError("没有找到 model.model.layers，请检查模型结构是否为 DeepseekV2ForCausalLM。")


def register_pre_hook_compat(module, hook_fn):
    """
    兼容不同 PyTorch 版本的 forward_pre_hook。
    hook_fn 统一签名：hook_fn(module, args, kwargs)
    """
    try:
        return module.register_forward_pre_hook(hook_fn, with_kwargs=True)
    except TypeError:
        def wrapper(module, args):
            return hook_fn(module, args, {})
        return module.register_forward_pre_hook(wrapper)


def cosine_importance(x, y, valid_mask=None):
    """
    x: [batch, seq, heads, dim]
    y: [batch, seq, heads, dim]

    similarity = mean cosine_similarity(x, y)
    importance = 1 - similarity

    cosine 越低，importance 越高。
    """
    x = x.float()
    y = y.float()

    dim = min(x.shape[-1], y.shape[-1])
    x = x[..., :dim]
    y = y[..., :dim]

    sim = F.cosine_similarity(x, y, dim=-1, eps=1e-6)  # [B, T, H]

    if valid_mask is not None:
        mask = valid_mask.to(sim.device).float()  # [B, T]
        mask = mask.unsqueeze(-1)                # [B, T, 1]
        sim = (sim * mask).sum(dim=(0, 1)) / mask.sum(dim=(0, 1)).clamp_min(1.0)
    else:
        sim = sim.mean(dim=(0, 1))

    importance = 1.0 - sim  # [H]
    return importance.detach().cpu()


def collect_head_importance(model, inputs, input_mode="hidden_split"):
    layers = get_decoder_layers(model)
    num_layers = len(layers)

    first_attn = layers[0].self_attn
    num_heads = int(first_attn.num_heads)

    importance_matrix = torch.full((num_layers, num_heads), float("nan"))
    cached_inputs = {}
    hooks = []

    valid_mask = inputs.get("attention_mask", None)
    if valid_mask is not None:
        valid_mask = valid_mask.detach()

    def make_attn_input_hook(layer_idx, attn_module):
        def hook(module, args, kwargs):
            hidden_states = kwargs.get("hidden_states", None)
            if hidden_states is None:
                hidden_states = args[0]

            # hidden_states: [B, T, hidden_size]
            bsz, seq_len, hidden_size = hidden_states.shape
            h = int(attn_module.num_heads)
            d = int(attn_module.v_head_dim)

            required = h * d
            if hidden_size < required:
                raise RuntimeError(
                    f"hidden_size={hidden_size} 小于 num_heads*v_head_dim={required}"
                )

            # 每个 head 的输入向量：[B, T, H, D]
            # DeepSeek-V2-Lite: hidden_size=2048, heads=16, v_head_dim=128，正好可切分
            x = hidden_states[..., :required].view(bsz, seq_len, h, d)
            cached_inputs[layer_idx] = x.detach()
        return hook

    def make_q_hook(layer_idx, attn_module):
        def hook(module, args, output):
            # q_proj/q_b_proj 输出：[B, T, H * q_head_dim]
            q = output
            if isinstance(q, tuple):
                q = q[0]

            bsz, seq_len, hidden = q.shape
            h = int(attn_module.num_heads)
            q_dim = hidden // h

            # DeepSeek-V2-Lite 的 q_head_dim = qk_nope_head_dim + qk_rope_head_dim。
            # v_head_dim=128；默认取 query 的前 v_head_dim 维作为 content 输入。
            d = min(int(attn_module.v_head_dim), q_dim)
            q = q.view(bsz, seq_len, h, q_dim)[..., :d]
            cached_inputs[layer_idx] = q.detach()
        return hook

    def make_o_proj_input_hook(layer_idx, attn_module):
        def hook(module, args, kwargs):
            if not args:
                return

            # o_proj 的输入就是拼接后的每头 attention 输出，形状 [B, T, H * v_head_dim]
            y_flat = args[0].detach()
            bsz, seq_len, hidden = y_flat.shape

            h = int(attn_module.num_heads)
            d = int(attn_module.v_head_dim)
            expected = h * d

            if hidden != expected:
                raise RuntimeError(
                    f"第 {layer_idx} 层 o_proj 输入维度为 {hidden}，"
                    f"但 num_heads*v_head_dim={expected}"
                )

            y = y_flat.view(bsz, seq_len, h, d)

            if layer_idx not in cached_inputs:
                raise RuntimeError(
                    f"第 {layer_idx} 层没有捕获到 attention head 输入。"
                )

            x = cached_inputs.pop(layer_idx)
            scores = cosine_importance(x, y, valid_mask=valid_mask)
            importance_matrix[layer_idx] = scores
        return hook

    for layer_idx, layer in enumerate(layers):
        attn = layer.self_attn

        if input_mode == "hidden_split":
            hooks.append(
                register_pre_hook_compat(
                    attn,
                    make_attn_input_hook(layer_idx, attn),
                )
            )
        else:
            # DeepSeek-V2-Lite q_lora_rank=None，所以通常是 q_proj；
            # 其他 DeepSeek-V2 变体可能是 q_b_proj。
            if hasattr(attn, "q_proj"):
                hooks.append(attn.q_proj.register_forward_hook(make_q_hook(layer_idx, attn)))
            elif hasattr(attn, "q_b_proj"):
                hooks.append(attn.q_b_proj.register_forward_hook(make_q_hook(layer_idx, attn)))
            else:
                raise RuntimeError(f"第 {layer_idx} 层没有找到 q_proj 或 q_b_proj。")

        hooks.append(
            register_pre_hook_compat(
                attn.o_proj,
                make_o_proj_input_hook(layer_idx, attn),
            )
        )

    model.eval()
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
        _ = model(
            **inputs,
            use_cache=False,
            output_attentions=False,
            output_hidden_states=False,
            return_dict=True,
        )

    for h in hooks:
        h.remove()

    if torch.isnan(importance_matrix).any():
        missing = torch.isnan(importance_matrix).any(dim=1).nonzero().flatten().tolist()
        raise RuntimeError(f"以下层没有成功计算 importance：{missing}")

    return importance_matrix.numpy()


def normalize_minmax(mat):
    lo = np.nanmin(mat)
    hi = np.nanmax(mat)
    if hi - lo < 1e-12:
        return np.zeros_like(mat)
    return (mat - lo) / (hi - lo)


def plot_matrix(mat, out_path, title):
    num_layers, num_heads = mat.shape

    plt.figure(figsize=(max(9, num_heads * 0.55), max(7, num_layers * 0.28)))
    im = plt.imshow(mat, aspect="auto", interpolation="nearest")

    plt.colorbar(im, label="Head importance")
    plt.xlabel("Attention head index")
    plt.ylabel("Layer index")
    plt.title(title)

    plt.xticks(np.arange(num_heads), [str(i) for i in range(num_heads)])
    plt.yticks(np.arange(num_layers), [str(i) for i in range(num_layers)])

    plt.tight_layout()
    plt.savefig(out_path, dpi=220)
    plt.close()

def locate_first_nan(model, inputs):
    layers = get_decoder_layers(model)
    handles = []

    def finite_status(t):
        if t is None or not torch.is_tensor(t):
            return "not_tensor"
        return {
            "shape": tuple(t.shape),
            "dtype": str(t.dtype),
            "device": str(t.device),
            "finite": bool(torch.isfinite(t).all().item()),
            "nan_count": int(torch.isnan(t).sum().item()),
            "inf_count": int(torch.isinf(t).sum().item()),
            "max_abs": float(torch.nan_to_num(t.float()).abs().max().item()),
        }

    def extract_tensor(output):
        if torch.is_tensor(output):
            return output
        if isinstance(output, (tuple, list)):
            for item in output:
                if torch.is_tensor(item):
                    return item
        return None

    def make_hook(name):
        def hook(module, args, output):
            inp = args[0] if len(args) > 0 and torch.is_tensor(args[0]) else None
            out = extract_tensor(output)

            inp_status = finite_status(inp)
            out_status = finite_status(out)

            inp_bad = isinstance(inp_status, dict) and not inp_status["finite"]
            out_bad = isinstance(out_status, dict) and not out_status["finite"]

            if inp_bad or out_bad:
                print(f"\nNaN/Inf detected at: {name}")
                print("input :", inp_status)
                print("output:", out_status)
                raise RuntimeError(f"first bad tensor around {name}")

        return hook

    for i, layer in enumerate(layers):
        handles.append(layer.register_forward_hook(make_hook(f"layer_{i}")))
        handles.append(layer.self_attn.register_forward_hook(make_hook(f"layer_{i}.self_attn")))
        handles.append(layer.self_attn.o_proj.register_forward_hook(make_hook(f"layer_{i}.self_attn.o_proj")))
        handles.append(layer.mlp.register_forward_hook(make_hook(f"layer_{i}.mlp")))

    try:
        model.eval()
        with torch.inference_mode():
            _ = model(
                **inputs,
                use_cache=False,
                output_attentions=False,
                output_hidden_states=False,
                return_dict=True,
            )
        print("No NaN/Inf found.")
    finally:
        for h in handles:
            h.remove()

def main():
    model_name = "/data/DeepSeek-Coder-V2-Lite-Base"

    # "hidden_split: 将 self_attn 输入 hidden_states 按 head 切分作为每头输入；"
    # "q_content: 使用 q_proj/q_b_proj 的 query 内容子空间作为每头输入。"
    input_mode = "hidden_split"

    csv_path = "deepseek_v2_lite_head_importance.csv"

    png_path = "deepseek_v2_lite_head_importance.png"

    # "--normalize", 是否将矩阵 min-max 归一化到 [0, 1] 后再画图；CSV 总是保存原始值
    action = "store_true"

    # input_text = "The internet, a global network connecting billions of devices"
    prompt = '''The internet, a global network connecting billions of devices, has profoundly reshaped nearly every aspect of modern life. Its origins, however, are surprisingly modest.  The story begins in the Cold War era, with the U.S. Department of Defense’s Advanced Research Projects Agency (ARPA).  In 1969, ARPA created ARPANET, a project designed to enable researchers to share computer resources. This initial network connected just four universities: UCLA, Stanford Research Institute, UC Santa Barbara, and the University of Utah. The primary goal wasn’t about cat videos or social media – it was about creating a decentralized communication system that could withstand a potential Soviet attack.  If one part of the network went down, others would remain operational.

Throughout the 1970s, ARPANET evolved, with the development of crucial protocols like TCP/IP (Transmission Control Protocol/Internet Protocol), which became the standard for communication over the network.  Email also emerged as a key application, fundamentally changing how people communicated professionally and personally.  However, access remained largely limited to academic and governmental institutions.

The 1980s saw the transition from ARPANET to the modern internet.  The National Science Foundation (NSF) played a crucial role, establishing NSFNET, a high-speed network connecting supercomputer centers across the United States. This significantly expanded network capacity and accessibility.  Crucially, NSFNET lifted restrictions on commercial traffic, paving the way for the internet’s commercialization.

The invention of the World Wide Web in 1989 by Tim Berners-Lee at CERN, the European Organization for Nuclear Research, was a watershed moment. Berners-Lee created the three fundamental technologies that underpin the Web: HTML (HyperText Markup Language), URL (Uniform Resource Locator), and HTTP (Hypertext Transfer Protocol). These allowed for the creation of interconnected documents and easily navigable information. The first web browser, WorldWideWeb (later renamed Nexus), was also developed.

The 1990s witnessed the explosive growth of the internet, fueled by the release of user-friendly browsers like Mosaic and Netscape Navigator.  The dot-com boom saw a surge of investment in internet-based companies, although many ultimately failed.  Despite the bubble burst, the underlying infrastructure and user base continued to expand rapidly.

Today, the internet is an integral part of global society. It facilitates communication, commerce, education, entertainment, and countless other activities.  Social media platforms connect billions of people worldwide, while e-commerce has revolutionized retail. The rise of mobile devices and wireless internet access has further extended the internet’s reach, making it accessible to an unprecedented number of people.

However, the internet also presents significant challenges. Concerns about privacy, security, misinformation, and digital inequality remain pressing issues. The future of the internet will likely involve ongoing debates about net neutrality, data governance, and the ethical implications of artificial intelligence.  Nevertheless, the internet's impact on humanity is undeniable and continues to unfold.'''


    if not torch.cuda.is_available():
        print("警告：没有检测到 CUDA。DeepSeek-V2-Lite-Chat 很大，CPU 基本不可行。")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True,)

    model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map="cpu",
            dtype=torch.float32,   # 关键
            low_cpu_mem_usage=True,
            attn_implementation="eager",
        )

    model.config.use_cache = False

    inputs = build_chat_inputs(tokenizer, prompt)

    # 对于 device_map="auto"，输入放到 embedding 所在设备即可
    input_device = model.get_input_embeddings().weight.device

    inputs = {k: v.to(input_device) for k, v in inputs.items()}

    locate_first_nan(model, inputs)

    importance = collect_head_importance(
        model=model,
        inputs=inputs,
        input_mode=input_mode,
    )

    np.savetxt(
        csv_path,
        importance,
        delimiter=",",
        header=",".join([f"head_{i}" for i in range(importance.shape[1])]),
        comments="",
    )

    # plot_data = normalize_minmax(importance) if action else importance
    plot_data = importance

    title = (
        f"DeepSeek-V2-Lite-Chat head importance\n"
        f"importance = 1 - mean cosine(input, output), input_mode={input_mode}"
    )
    if action:
        title += ", min-max normalized"

    plot_matrix(plot_data, png_path, title)

    print(f"完成：矩阵图已保存到 {png_path}")
    print(f"完成：原始 importance 矩阵已保存到 {csv_path}")
    print(f"矩阵形状：{importance.shape}，即 layer × head")


if __name__ == "__main__":
    main()
