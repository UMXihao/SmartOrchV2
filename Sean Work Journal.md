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