//
// Created by lili-5090 on 2026/5/16.
//
// examples/head-importance/head-importance.cpp

#include "../../ggml/include/ggml.h"
#include "arg.h"
#include "common.h"
#include "ggml-backend.h"
#include "ggml.h"
#include "log.h"
#include "llama.h"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

struct HeadStat {
    double jsd_sum = 0.0;
    uint64_t count = 0;
};

struct CallbackState {
    int n_layer = 0;
    int n_head = 0;
    int head_dim = 0;

    std::vector<HeadStat> stats;

    // per layer cached Vcur tensor, flattened as float
    std::vector<std::vector<float>> vcur_by_layer;
    std::vector<int64_t> v_ne0;
    std::vector<int64_t> v_ne1;
    std::vector<int64_t> v_ne2;
};

static int parse_layer_id(const std::string & name) {
    std::smatch m;

    std::regex r1("^Vcur_cont-([0-9]+)$");
    if (std::regex_match(name, m, r1)) {
        return std::stoi(m[1]);
    }

    std::regex r2("^kqv-([0-9]+) \\(permuted\\)$");
    if (std::regex_match(name, m, r2)) {
        return std::stoi(m[1]);
    }

    return -1;
}

static bool is_vcur_name(const std::string & name) {
    return std::regex_match(name, std::regex("^Vcur_cont-[0-9]+$"));
}

static bool is_attn_out_name(const std::string & name) {
    return std::regex_match(name, std::regex("^kqv-[0-9]+ \\(permuted\\)$"));
}

static std::vector<float> tensor_to_f32(struct ggml_tensor * t) {
    const size_t nbytes = ggml_nbytes(t);
    const int64_t n = ggml_nelements(t);

    std::vector<uint8_t> raw(nbytes);
    ggml_backend_tensor_get(t, raw.data(), 0, nbytes);

    std::vector<float> out(n);

    if (t->type == GGML_TYPE_F32) {
        std::memcpy(out.data(), raw.data(), n * sizeof(float));
        return out;
    }

    if (t->type == GGML_TYPE_F16) {
        const ggml_fp16_t * p = reinterpret_cast<const ggml_fp16_t *>(raw.data());
        for (int64_t i = 0; i < n; ++i) {
            out[i] = ggml_fp16_to_fp32(p[i]);
        }
        return out;
    }

    // 激活通常是 f32/f16；其他类型先报错，避免默默算错
    std::cerr << "Unsupported activation tensor type: "
              << ggml_type_name(t->type) << "\n";
    return {};
}

static void softmax_slice(
    const std::vector<float> & x,
    int64_t offset,
    int64_t stride,
    int64_t len,
    std::vector<double> & p
) {
    p.resize(len);

    double mx = -1e300;
    for (int64_t i = 0; i < len; ++i) {
        mx = std::max(mx, static_cast<double>(x[offset + i * stride]));
    }

    double s = 0.0;
    for (int64_t i = 0; i < len; ++i) {
        p[i] = std::exp(static_cast<double>(x[offset + i * stride]) - mx);
        s += p[i];
    }

    const double eps = 1e-12;
    for (int64_t i = 0; i < len; ++i) {
        p[i] = std::max(p[i] / s, eps);
    }
}

static double jsd(const std::vector<double> & p, const std::vector<double> & q) {
    const double eps = 1e-12;
    double v = 0.0;

    for (size_t i = 0; i < p.size(); ++i) {
        const double pi = std::max(p[i], eps);
        const double qi = std::max(q[i], eps);
        const double m = 0.5 * (pi + qi);

        v += 0.5 * pi * std::log(pi / m);
        v += 0.5 * qi * std::log(qi / m);
    }

    return v;
}

static void accumulate_layer(
    CallbackState & st,
    int layer,
    const std::vector<float> & vcur,
    const std::vector<float> & out,
    int64_t ne0,
    int64_t ne1,
    int64_t ne2
) {
    // 期望形状：[head_dim, n_head, n_tokens, 1]
    const int64_t head_dim = ne0;
    const int64_t n_head = ne1;
    const int64_t n_tok = ne2;

    if (layer < 0 || layer >= st.n_layer) return;
    if (n_head != st.n_head) return;
    if (head_dim <= 0 || n_tok <= 0) return;

    std::vector<double> p, q;

    for (int64_t t = 0; t < n_tok; ++t) {
        for (int64_t h = 0; h < n_head; ++h) {
            const int64_t offset = t * n_head * head_dim + h * head_dim;

            softmax_slice(vcur, offset, 1, head_dim, p);
            softmax_slice(out,  offset, 1, head_dim, q);

            const double d = jsd(p, q);
            auto & cell = st.stats[layer * st.n_head + h];
            cell.jsd_sum += d;
            cell.count += 1;
        }
    }
}

static bool cb_eval(struct ggml_tensor * t, bool ask, void * user_data) {
    CallbackState * st = reinterpret_cast<CallbackState *>(user_data);
    const std::string name = t->name ? std::string(t->name) : "";

    const bool want = is_vcur_name(name) || is_attn_out_name(name);

    if (ask) {
        return want;
    }

    if (!want) {
        return true;
    }

    const int layer = parse_layer_id(name);
    if (layer < 0 || layer >= st->n_layer) {
        return true;
    }

    auto data = tensor_to_f32(t);
    if (data.empty()) {
        return true;
    }

    const int64_t ne0 = t->ne[0];
    const int64_t ne1 = t->ne[1];
    const int64_t ne2 = t->ne[2];

    if (is_vcur_name(name)) {
        st->vcur_by_layer[layer] = std::move(data);
        st->v_ne0[layer] = ne0;
        st->v_ne1[layer] = ne1;
        st->v_ne2[layer] = ne2;
        return true;
    }

    if (is_attn_out_name(name)) {
        const auto & vcur = st->vcur_by_layer[layer];
        if (!vcur.empty()) {
            accumulate_layer(*st, layer, vcur, data, ne0, ne1, ne2);
        }
        return true;
    }

    return true;
}

static std::string extract_prompt_from_jsonl(const std::string & line) {
    const std::string key = "\"prompt\"";
    auto p = line.find(key);
    if (p == std::string::npos) return "";

    p = line.find(':', p);
    if (p == std::string::npos) return "";

    p = line.find('"', p);
    if (p == std::string::npos) return "";

    std::string out;
    bool esc = false;

    for (size_t i = p + 1; i < line.size(); ++i) {
        char c = line[i];

        if (esc) {
            if (c == 'n') out.push_back('\n');
            else if (c == 't') out.push_back('\t');
            else out.push_back(c);
            esc = false;
        } else {
            if (c == '\\') esc = true;
            else if (c == '"') break;
            else out.push_back(c);
        }
    }

    return out;
}

static bool eval_prompt(llama_context * ctx, const common_params & params, const std::string & prompt) {
    const llama_model * model = llama_get_model(ctx);
    const llama_vocab * vocab = llama_model_get_vocab(model);

    const bool add_bos = llama_vocab_get_add_bos(vocab);
    std::vector<llama_token> tokens = common_tokenize(ctx, prompt, add_bos, true);

    if (tokens.empty()) {
        return false;
    }

    if ((int)tokens.size() > params.n_ctx) {
        tokens.resize(params.n_ctx);
    }

    llama_memory_clear(llama_get_memory(ctx), true);

    llama_batch batch = llama_batch_get_one(tokens.data(), tokens.size());

    // 只需要前向，不需要生成
    const int rc = llama_decode(ctx, batch);
    return rc == 0;
}

static void write_csv(const std::string & path, const CallbackState & st) {
    std::ofstream f(path);
    f << "layer,head,importance,similarity,mean_jsd,n_prompts_or_windows,n_token_vectors\n";

    const double log2v = std::log(2.0);

    for (int l = 0; l < st.n_layer; ++l) {
        for (int h = 0; h < st.n_head; ++h) {
            const auto & s = st.stats[l * st.n_head + h];

            double mean_jsd = s.count ? s.jsd_sum / static_cast<double>(s.count) : 0.0;
            double importance = mean_jsd / log2v;
            double similarity = 1.0 - importance;

            f << l << ","
              << h << ","
              << importance << ","
              << similarity << ","
              << mean_jsd << ","
              << 0 << ","
              << s.count << "\n";
        }
    }
}

static void print_usage(int argc, char ** argv) {
    (void) argc;

    LOG("\nexample usage:\n");
    LOG("\n  text generation:     %s -m your_model.gguf -p \"I believe the meaning of life is\" -n 128 -no-cnv\n", argv[0]);
    LOG("\n  chat (conversation): %s -m your_model.gguf -sys \"You are a helpful assistant\"\n", argv[0]);
    LOG("\n");
}

int main(int argc, char ** argv) {
    common_params params;
    common_init();

    if (!common_params_parse(argc, argv, params, LLAMA_EXAMPLE_COMMON, print_usage)) {
        return 1;
    }

    std::string jsonl = "/home/lili-5090/Sean/SmartOrchV2/scripts/attn-head/squad_validation_test.jsonl";
    std::string out_csv = "head_importance.csv";

    llama_backend_init();
    llama_numa_init(params.numa);

    // 为了稳定捕获普通 attention 中间张量，建议关闭 flash attention
    params.flash_attn_type = LLAMA_FLASH_ATTN_TYPE_DISABLED;
    params.warmup = false;

    CallbackState st;

    params.cb_eval = cb_eval;
    params.cb_eval_user_data = &st;

    llama_model * model = nullptr;
    llama_context * ctx = nullptr;

    auto llama_init = common_init_from_params(params);
    model = llama_init.model.get();
    ctx = llama_init.context.get();

    if (!model || !ctx) {
        std::cerr << "failed to load model/context\n";
        return 1;
    }

    st.n_layer = llama_model_n_layer(model);
    st.n_head = llama_model_n_head(model);
    st.stats.resize(st.n_layer * st.n_head);
    st.vcur_by_layer.resize(st.n_layer);
    st.v_ne0.resize(st.n_layer);
    st.v_ne1.resize(st.n_layer);
    st.v_ne2.resize(st.n_layer);

    std::cerr << "n_layer=" << st.n_layer
              << " n_head=" << st.n_head << "\n";

    std::ifstream in(jsonl);
    std::string line;
    uint64_t n_prompt = 0;

    while (std::getline(in, line)) {
        std::string prompt = extract_prompt_from_jsonl(line);
        if (prompt.empty()) continue;

        for (auto & v : st.vcur_by_layer) {
            v.clear();
        }

        if (eval_prompt(ctx, params, prompt)) {
            n_prompt++;
        }

        if (n_prompt % 100 == 0) {
            std::cerr << "processed prompts: " << n_prompt << "\n";
            write_csv(out_csv, st);
        }
    }

    write_csv(out_csv, st);

    llama_free(ctx);
    llama_model_free(model);
    llama_backend_free();

    std::cerr << "done. prompts=" << n_prompt
              << " csv=" << out_csv << "\n";

    return 0;
}