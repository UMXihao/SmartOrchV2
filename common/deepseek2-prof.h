#pragma once

#include "ggml.h"
#include "ggml-backend.h"

#include <cstdint>
#include <mutex>
#include <string>
#include <unordered_map>

struct ds2_prof_counter {
    uint64_t n        = 0;
    uint64_t total_us = 0;
    uint64_t min_us   = UINT64_MAX;
    uint64_t max_us   = 0;

    void add(uint64_t us) {
        n++;
        total_us += us;
        if (us < min_us) min_us = us;
        if (us > max_us) max_us = us;
    }

    double avg_us() const {
        return n ? double(total_us) / double(n) : 0.0;
    }
};

struct ds2_prof_state {
    std::mutex mtx;

    std::unordered_map<int, uint64_t> attn_start_us;
    std::unordered_map<int, uint64_t> moe_start_us;
    std::unordered_map<int, uint64_t> shexp_start_us;
    std::unordered_map<int, uint64_t> expert_total_start_us;

    ds2_prof_counter attn_total;
    ds2_prof_counter moe_routed_expert;
    ds2_prof_counter shared_expert;
    ds2_prof_counter expert_total;

    uint64_t observed_events = 0;
    uint64_t dump_every = 512;
};

bool llama_deepseek2_prof_cb(struct ggml_tensor * t, bool ask, void * user_data);

void llama_deepseek2_prof_dump(ds2_prof_state & st);