# Cross-compile using Android NDK

Note(Sean): I do not Build on Android using Termux, because I don't want to consume the memory using static code. 

## CPU ABI
How to use adb to find the CPU ABI?

$`adb shell getprop ro.product.cpu.abi`

arm64-v8a

## GPU Specification

How to use adb to find the GPU specification？

`$ adb shell dumpsys | grep GLES`

GLES: Qualcomm, Adreno (TM) 750, OpenGL ES 3.2 V@0762.10 (GIT@1394a2c7a8, Id12349e41b, 1708672982) (Date:02/23/24)

*Qualcomm, Adreno (TM) 750, OpenGL ES 3.2 V@0762.10* is the GPU specification.

## Start to Build 

Set env var.

`$ export ANDROID_NDK={ANDROID_NDK_PATH}`

`$ export ANDROID_NDK=/home/lili-5090/Sean/android-ndk-r27d
`

```
$ cmake \
-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DCMAKE_C_FLAGS="-march=armv8.7a" \
-DCMAKE_CXX_FLAGS="-march=armv8.7a" \
-DGGML_OPENMP=OFF \
-DGGML_LLAMAFILE=OFF \
-DLLAMA_CURL=OFF \
-B build-android
```

```
$ mkdir smartorch-cpu
$ cmake --build build-android --config Release -j 22
$ cmake --install build-android --prefix install/ --config Release
```

After installing, go ahead and download the model of your choice to your host system. Then:


```
$ adb push smartorch-cpu /data/local/tmp/
$ adb push {model}.gguf /data/local/tmp/models
$ adb shell
```

In the `adb shell`:

```
$ cd /data/local/tmp/smartorch-cpu
$ LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/{model}.gguf -n {output-length} -no-cnv -p "{your-prompt}"
```

GPU Compile

未添加OpenCL ~/android-ndk-r27d/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/
已添加OpenCL ~/Hexagon_SDK/6.4.0.2/tools/android-ndk-r25c/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib/aarch64-linux-android




cmake --build build-android --config Release -j 22

```
cmake \
-DCMAKE_TOOLCHAIN_FILE=$HOME/Sean/Hexagon_SDK/6.4.0.2/tools/android-ndk-r25c/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF \
-B build-android

rm -rf kernel
mkdir kernel

cmake --build build-android --config Release -j 22

cmake --install build-android --prefix kernel/ --config Release

adb -s 3B15BC00X7Q00000 push kernel/ /data/local/tmp/

adb -s 3B15BC00X7Q00000 shell

cd /data/local/tmp/kernel

LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 10 -no-cnv -f ../split-cpu/fix-token.txt --no-display-prompt --no-warmup -ngl 30
```


## Access the server started on the mobile phone from the computer.

- mobile phone:

    LD_LIBRARY_PATH=lib ./bin/llama-server -m {model}.gguf --host 0.0.0.0 --port 8080

- computer
  
    adb forward tcp:8080 tcp:8080

### CPU fix-token.py
- TTFT:  31568.559 TPOT:  124.0401328125
- TTFT:  22969.977 TPOT:  129.466625
- TTFT:  22809.283 TPOT:  127.6569140625
- TTFT:  22953.495 TPOT:  120.2772890625
- TTFT:  22871.363 TPOT:  127.8050625
- TTFT:  22826.562 TPOT:  116.590703125
- TTFT:  22842.857 TPOT:  124.4898671875
- TTFT:  23088.147 TPOT:  116.120453125
- TTFT:  23005.06 TPOT:  119.671421875
- TTFT:  22887.41 TPOT:  119.1555703125
- Average TTFT:  23782.2713 Average TPOT:  122.52740390624999

### GPU fix-token.py
- TTFT:  249061.785 TPOT:  4014.5581953125
- TTFT:  39570.814 TPOT:  2532.0164140625
- TTFT:  39665.166 TPOT:  2522.842015625
- TTFT:  39354.19 TPOT:  2542.9343203125
- TTFT:  40021.348 TPOT:  2514.841390625
- TTFT:  39375.833 TPOT:  2562.2161484375
- TTFT:  55456.788 TPOT:  2559.3320078125
- TTFT:  40126.243 TPOT:  2512.08775
- TTFT:  40570.132 TPOT:  2561.249578125
- TTFT:  55383.31 TPOT:  2561.2100390625
- Average TTFT:  63858.5609 Average TPOT:  2688.3287859375

```
[split-node] split=1666 backend=OpenCL name=norm-26 op=RMS_NORM
[split-node] split=1667 backend=OpenCL name=attn_norm-26 op=MUL
[split-node] split=1668 backend=OpenCL name=q-26 op=MUL_MAT
[split-node] split=1669 backend=OpenCL name=q_pe-26 op=VIEW
[split-node] split=1670 backend=OpenCL name=q_pe-26 op=ROPE
[split-node] split=1671 backend=OpenCL name=q_nope-26 op=VIEW
[split-node] split=1672 backend=OpenCL name=Qcur-26 op=CONCAT
[split-node] split=1673 backend=OpenCL name=kv_cmpr_pe-26 op=MUL_MAT
[split-node] split=1674 backend=OpenCL name=k_pe-26 op=VIEW
[split-node] split=1675 backend=OpenCL name=k_pe-26 op=ROPE
[split-node] split=1676 backend=OpenCL name=node_1677 op=REPEAT
[split-node] split=1677 backend=OpenCL name=kv_cmpr-26 op=VIEW
[split-node] split=1678 backend=OpenCL name=norm-26 op=RMS_NORM
[split-node] split=1679 backend=OpenCL name=kv_cmpr-26 op=MUL
[split-node] split=1680 backend=OpenCL name=kv-26 op=MUL_MAT
[split-node] split=1681 backend=OpenCL name=k_nope_view-26 op=VIEW
[split-node] split=1682 backend=OpenCL name=Kcur-26 op=CONCAT
[split-node] split=1683 backend=OpenCL name=Vcur_view-26 op=VIEW
[split-node] split=1684 backend=OpenCL name=Vcur_cont-26 op=CONT
[split-node] split=1685 backend=OpenCL name=Kcur-26 (view) op=VIEW
[split-node] split=1686 backend=OpenCL name=cache_k_l26 (view) op=SET_ROWS
[split-node] split=1687 backend=OpenCL name=Vcur_cont-26 (view) op=VIEW
[split-node] split=1688 backend=OpenCL name=cache_v_l26 (view) op=SET_ROWS
[split-node] split=1689 backend=OpenCL name=Qcur-26 (view) op=VIEW
[split-node] split=1690 backend=OpenCL name=Qcur-26 (view) (permuted) op=PERMUTE
[split-node] split=1691 backend=OpenCL name=cache_k_l26 (view) op=VIEW
[split-node] split=1692 backend=OpenCL name=cache_k_l26 (view) (permuted) op=PERMUTE
[split-node] split=1693 backend=OpenCL name=cache_v_l26 (view) op=VIEW
[split-node] split=1694 backend=OpenCL name=cache_v_l26 (view) (permuted) op=PERMUTE
[split-node] split=1695 backend=OpenCL name=__fattn__-26 op=FLASH_ATTN_BACK
[split-node] split=1696 backend=OpenCL name=kqv_out-26 op=RESHAPE
[split-node] split=1697 backend=OpenCL name=node_1698 op=MUL_MAT
[split-node] split=1698 backend=OpenCL name=node_1699 op=GET_ROWS
[split-node] split=1699 backend=OpenCL name=node_1700 op=GET_ROWS
[split-node] split=1700 backend=OpenCL name=ffn_inp-26 op=ADD
[split-node] split=1701 backend=OpenCL name=norm-26 op=RMS_NORM
[split-node] split=1702 backend=OpenCL name=ffn_norm-26 op=MUL
[split-node] split=1703 backend=OpenCL name=ffn_moe_logits-26 op=MUL_MAT
[split-node] split=1704 backend=OpenCL name=ffn_moe_probs-26 op=SOFT_MAX
[split-node] split=1705 backend=OpenCL name=ffn_moe_probs-26 (reshaped) op=RESHAPE

## ggml_top_k
[split-node] split=1706 backend=OpenCL name=ffn_moe_argsort-26 op=ARGSORT
[split-node] split=1707 backend=OpenCL name=ffn_moe_topk-26 op=VIEW
[split-node] split=1708 backend=OpenCL name=ffn_moe_weights-26 op=GET_ROWS
[split-node] split=1709 backend=OpenCL name=ffn_moe_weights_scaled-26 op=SCALE
[split-node] split=1710 backend=OpenCL name=ffn_norm-26 (reshaped) op=RESHAPE

## selected_expert
[split-node] split=1711 backend=OpenCL name=ffn_moe_gate-26 op=MUL_MAT_ID
[split-node] split=1712 backend=OpenCL name=ffn_moe_up-26 op=MUL_MAT_ID
[split-node] split=1713 backend=OpenCL name=ffn_moe_weighted-26 op=(null)
[split-node] split=1714 backend=OpenCL name=ffn_moe_down-26 op=MUL_MAT_ID
[split-node] split=1715 backend=OpenCL name=node_1716 op=MUL
[split-node] split=1716 backend=OpenCL name= (view) op=VIEW
[split-node] split=1717 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=1718 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=1719 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=1720 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=1721 backend=OpenCL name=node_1716 (view) op=VIEW
[split-node] split=1722 backend=OpenCL name=ffn_gate-26 op=MUL_MAT
[split-node] split=1723 backend=OpenCL name=ffn_up-26 op=MUL_MAT
[split-node] split=1724 backend=OpenCL name=ffn_swiglu-26 op=(null)
[split-node] split=1725 backend=OpenCL name=node_1726 op=ADD
[split-node] split=1726 backend=OpenCL name=node_1727 op=ADD
[split-node] split=1727 backend=OpenCL name=node_1728 op=ADD
[split-node] split=1728 backend=OpenCL name=node_1729 op=ADD
[split-node] split=1729 backend=OpenCL name=ffn_moe_out-26 op=ADD
[split-node] split=1730 backend=OpenCL name=ffn_shexp-26 op=MUL_MAT
[split-node] split=1731 backend=OpenCL name=ffn_out-26 op=ADD
[split-node] split=1732 backend=OpenCL name=l_out-26 op=ADD
[split-node] split=1733 backend=OpenCL name=norm op=RMS_NORM
[split-node] split=1734 backend=OpenCL name=result_norm op=MUL
[split-node] split=1735 backend=OpenCL name=result_output op=MUL_MAT
```

## Custom Expert Number
--override-kv deepseek2.expert_used_count=int:4

## Add compile param
cmake -B build \
-DCMAKE_C_FLAGS="-DLLAMA_BACK_CPU" \
-DCMAKE_CXX_FLAGS="-DLLAMA_BACK_CPU"

cmake -B build \
-DCMAKE_C_FLAGS="-DLLAMA_OPENCL_KERNEL_LAUNCHES" \
-DCMAKE_CXX_FLAGS="-DLLAMA_OPENCL_KERNEL_LAUNCHES"


### 5090 Compile
- Static Graph
```
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

- Dynamic Graph
```
cmake -B build -DGGML_CUDA=ON -DCMAKE_C_FLAGS="-DLLAMA_BACK_CPU" -DCMAKE_CXX_FLAGS="-DLLAMA_BACK_CPU"
cmake --build build --config Release
```


