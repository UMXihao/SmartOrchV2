// src/llama-moe-expert-stat.h

#pragma once

#include "ggml.h"
#include "ggml-backend.h"

#include <cstdint>
#include <vector>
#include <array>
#include <cstdio>
#include <stdexcept>

struct llama_moe_expert_stat {
    bool enabled = false;

    int n_layer = 0;
    int n_expert = 0;
    int n_expert_used = 0;

    // expert_mask[layer][expert_id] = true 表示该专家在 expert_list[layer] 中
    std::vector<std::vector<uint8_t>> expert_mask;

    std::vector<uint64_t> expert_sum;
    std::vector<uint64_t> token_number;

    void init(
        int n_layer_,
        int n_expert_,
        int n_expert_used_,
        const std::vector<std::vector<int>> & expert_list
    ) {
        n_layer = n_layer_;
        n_expert = n_expert_;
        n_expert_used = n_expert_used_;

        if ((int) expert_list.size() != n_layer) {
            throw std::runtime_error("expert_list size must equal n_layer");
        }

        expert_mask.assign(n_layer, std::vector<uint8_t>(n_expert, 0));
        expert_sum.assign(n_layer, 0);
        token_number.assign(n_layer, 0);

        for (int il = 0; il < n_layer; ++il) {
            for (int expert_id : expert_list[il]) {
                if (expert_id < 0 || expert_id >= n_expert) {
                    throw std::runtime_error("expert id out of range");
                }
                expert_mask[il][expert_id] = 1;
            }
        }

        enabled = true;
    }

    void reset() {
        std::fill(expert_sum.begin(), expert_sum.end(), 0);
        std::fill(token_number.begin(), token_number.end(), 0);
    }

    void collect_topk_tensor(int il, ggml_tensor * selected_experts) {
        if (!enabled || selected_experts == nullptr) {
            return;
        }

        if (il < 0 || il >= n_layer) {
            return;
        }

        // layer 0 in DeepSeek-V2-Lite is usually dense FFN, no MoE route.
        if (selected_experts->type != GGML_TYPE_I32) {
            throw std::runtime_error("selected_experts must be GGML_TYPE_I32");
        }

        const int64_t k        = selected_experts->ne[0]; // n_expert_used, usually 6
        const int64_t n_tokens = selected_experts->ne[1];

        // if (k != n_expert_used) {
        //     throw std::runtime_error("unexpected n_expert_used in selected_experts");
        // }

        std::vector<int32_t> ids(k * n_tokens);

        // OpenCL/GPU 后端下必须这样回读，不能直接读 selected_experts->data
        ggml_backend_tensor_get(
            selected_experts,
            ids.data(),
            0,
            ids.size() * sizeof(int32_t)
        );

        uint64_t local_sum = 0;

        for (int64_t t = 0; t < n_tokens; ++t) {
            for (int64_t j = 0; j < k; ++j) {
                const int expert_id = ids[t * k + j];

                if (expert_id >= 0 && expert_id < n_expert) {
                    local_sum += expert_mask[il][expert_id] ? 1 : 0;
                }
            }
        }

        expert_sum[il] += local_sum;
        token_number[il] += n_tokens;
    }

    void print(FILE * fp = stderr) const {
        if (!enabled) {
            return;
        }

        fprintf(fp, "\n=== MoE expert hit statistics ===\n");
        fprintf(fp, "layer\ttoken_number\texpert_sum\texpert_mean\texpert_hit_rate\n");

        for (int il = 0; il < n_layer; ++il) {
            const double mean = token_number[il] == 0
                ? 0.0
                : (double) expert_sum[il] / (double) token_number[il];

            const double hit_rate = n_expert_used == 0
                ? 0.0
                : mean / (double) n_expert_used;

            fprintf(
                fp,
                "%d\t%llu\t%llu\t%.6f\t%.6f\n",
                il,
                (unsigned long long) token_number[il],
                (unsigned long long) expert_sum[il],
                mean,
                hit_rate
            );
        }

        fprintf(fp, "=================================\n");
    }
};