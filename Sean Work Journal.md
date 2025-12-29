# 11-12-2025 

## Cross-compile using Android NDK, just use CPU.

Add docs/RealMe GT6 build.md

If you only use cpu to run a qwen2.5-0.5b-instruct.f16.gguf, it's very slow! Can't abide this speed!

```
llama_perf_sampler_print:    sampling time =       3.78 ms /    23 runs   (    0.16 ms per token,  6083.05 tokens per second)
llama_perf_context_print:        load time =   12328.11 ms
llama_perf_context_print: prompt eval time =   11696.29 ms /    13 tokens (  899.71 ms per token,     1.11 tokens per second)
llama_perf_context_print:        eval time =  104908.95 ms /     9 runs   (11656.55 ms per token,     0.09 tokens per second)
llama_perf_context_print:       total time =  134561.56 ms /    22 tokens
```

## Remove redundant scripts.

The script is retained as follows:
: llama-cli
: llama-mtmd-cli
: llama-quantize
: llama-server
: llama-simple

# 11-26-2025

## Debug-CUDA

1. Settings | Build, Execution, Deployment | CMake
2. CMake options: -DGGML_CUDA=ON
3. Re-build

## Run a MoE LLM and Skip Computing

DeepSeek-R1-Distill-Qwen-7B arch-name: LLM_ARCH_QWEN2 is a dense model.

DeepSeek-Coder-V2-Lite-Instruct arch-name: LLM_ARCH_DEEPSEEK2 is a MoE model.
64 Experts, use 6 experts.


## LLAMA_MOE_STATS only supports CPU backend.
```
cmake -B build \
-DCMAKE_C_FLAGS="-DLLAMA_MOE_STATS" \
-DCMAKE_CXX_FLAGS="-DLLAMA_MOE_STATS"

cmake --build build --config Release -j 8
```

# 12-23-2025
## Clion Compile Parameters
-DCMAKE_C_FLAGS="-DLLAMA_MOE_STATS" -DCMAKE_CXX_FLAGS="-DLLAMA_MOE_STATS"

-DGGML_CUDA=ON -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc

## HumanEval(Python) Evaluation Exception
read time out

# 12-24-2025
## [CPU] Specific experts for the task

Implementing index passing using op_params

To solve the timeout exception, increase timeout of human_eval.

## [CUDA] Specific experts for the task

# 12-29-2025
## Testing a new sentiment dataset
We test with a new sentiment categorical dataset IMDB, but the analysis time using CPU is still very long.

## Sparsity: Early Exit 
Skipping a specific layer requires modifying the computation graph and loading model parameters. 
For DeepSeekv2, the last layer cannot be skipped; otherwise, the output cannot be built.