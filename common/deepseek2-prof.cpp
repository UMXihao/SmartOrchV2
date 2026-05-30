#include "deepseek2-prof.h"

#include <algorithm>
#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <cstring>

static bool has_prefix(const char * s, const char * prefix) {
    return std::strncmp(s, prefix, std::strlen(prefix)) == 0;
}

static bool is_ds2_prof_marker(const char * name) {
    return has_prefix(name, "ds2_attn_start") ||
           has_prefix(name, "ds2_attn_end") ||
           has_prefix(name, "ds2_moe_start") ||
           has_prefix(name, "ds2_moe_end") ||
           has_prefix(name, "ds2_shexp_start") ||
           has_prefix(name, "ds2_shexp_end") ||
           has_prefix(name, "ds2_expert_total_start") ||
           has_prefix(name, "ds2_expert_total_end");
}

static int parse_layer_id(const char * name) {
    const int len = (int) std::strlen(name);
    int r = len - 1;

    while (r >= 0 && std::isdigit((unsigned char) name[r])) {
        r--;
    }

    if (r == len - 1) {
        return -1;
    }

    return std::atoi(name + r + 1);
}

static void maybe_dump(ds2_prof_state & st) {
    st.observed_events++;

    if (st.dump_every == 0) {
        return;
    }

    if (st.observed_events % st.dump_every == 0) {
        llama_deepseek2_prof_dump(st);
    }
}

static void finish_span(
        std::unordered_map<int, uint64_t> & start_map,
        int layer,
        uint64_t now,
        ds2_prof_counter & counter) {
    auto it = start_map.find(layer);
    if (it == start_map.end()) {
        return;
    }

    const uint64_t beg = it->second;
    start_map.erase(it);

    if (now >= beg) {
        counter.add(now - beg);
    }
}

bool llama_deepseek2_prof_cb(struct ggml_tensor * t, bool ask, void * user_data) {
    if (t == nullptr || user_data == nullptr) {
        return true;
    }

    const char * name = t->name;

    if (!is_ds2_prof_marker(name)) {
        return false;
    }

    // ask == true：告诉 scheduler 这个节点需要被观察，从而在这里切分 graph。
    if (ask) {
        return true;
    }

    auto * st = reinterpret_cast<ds2_prof_state *>(user_data);

    const uint64_t now = ggml_time_us();
    const int layer = parse_layer_id(name);

    {
        std::lock_guard<std::mutex> lock(st->mtx);

        if (has_prefix(name, "ds2_attn_start")) {
            st->attn_start_us[layer] = now;
        } else if (has_prefix(name, "ds2_attn_end")) {
            finish_span(st->attn_start_us, layer, now, st->attn_total);
        } else if (has_prefix(name, "ds2_moe_start")) {
            st->moe_start_us[layer] = now;
        } else if (has_prefix(name, "ds2_moe_end")) {
            finish_span(st->moe_start_us, layer, now, st->moe_routed_expert);
        } else if (has_prefix(name, "ds2_shexp_start")) {
            st->shexp_start_us[layer] = now;
        } else if (has_prefix(name, "ds2_shexp_end")) {
            finish_span(st->shexp_start_us, layer, now, st->shared_expert);
        } else if (has_prefix(name, "ds2_expert_total_start")) {
            st->expert_total_start_us[layer] = now;
        } else if (has_prefix(name, "ds2_expert_total_end")) {
            finish_span(st->expert_total_start_us, layer, now, st->expert_total);
        }

        maybe_dump(*st);
    }

    return true;
}

static void print_counter(const char * name, const ds2_prof_counter & c) {
    if (c.n == 0) {
        std::fprintf(stderr, "[ds2-prof] %-20s n=0\n", name);
        return;
    }

    std::fprintf(stderr,
            "[ds2-prof] %-20s n=%llu total=%.3f ms avg=%.3f ms min=%.3f ms max=%.3f ms\n",
            name,
            (unsigned long long) c.n,
            c.total_us / 1000.0,
            c.avg_us() / 1000.0,
            c.min_us / 1000.0,
            c.max_us / 1000.0);
}

void llama_deepseek2_prof_dump(ds2_prof_state & st) {
    std::fprintf(stderr, "\n========== DeepSeek2 module latency ==========\n");
    print_counter("attention_total",   st.attn_total);
    print_counter("moe_routed_expert",  st.moe_routed_expert);
    print_counter("shared_expert",      st.shared_expert);
    print_counter("expert_total",       st.expert_total);
    std::fprintf(stderr, "=============================================\n\n");
}