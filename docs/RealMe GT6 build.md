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

cmake --install build-android --prefix test-output/ --config Release

adb -s 3B15BC00X7Q00000 push kernel/ /data/local/tmp/

adb -s 3B15BC00X7Q00000 shell

cd /data/local/tmp/kernel

LD_LIBRARY_PATH=lib ./bin/llama-server -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 10 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30

LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf -n 10 -no-cnv -f ../models/fix-token.txt --no-display-prompt  -ngl 50 -c 4096

LD_LIBRARY_PATH=lib ./bin/llama-completion -m ../models/DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf -n 10 -no-cnv -f ../models/fix-token.txt --no-display-prompt  -ngl 50 -c 4096

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

## 静态图捕获 + 动态参数更新
### 5090 Compile
- Static Graph
```
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j 22
```

- Dynamic Graph
```
cmake -B build -DGGML_CUDA=ON -DCMAKE_C_FLAGS="-DLLAMA_BACK_CPU" -DCMAKE_CXX_FLAGS="-DLLAMA_BACK_CPU"
cmake --build build --config Release -j 22
```
- Static Graph Result
```
[split-run] id=0 copy=0.000 ms compute=0.112 ms total=0.112 ms
[split-run] id=1 copy=16.634 ms compute=8.129 ms total=24.763 ms
```

### CPU Compile
```
cmake -B build
cmake --build build --config Release -j 22
```
- Static Graph Result
```
[split-run] id=0 copy=0.000 ms compute=1250.716 ms total=1250.716 ms
```


### Win Compile Android GPU
```
# git bash execution

export ANDROID_NDK=~/Documents/Sean/android-sdk/ndk/26.3.11579264

mkdir build-android
cd build-android

cmake .. -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-28 \
  -DBUILD_SHARED_LIBS=OFF \
  -DGGML_OPENCL=ON \
  -DLLAMA_CURL=OFF \
  -DGGML_OPENMP=OFF
  
ninja

cd ..
mkdir win-gpu
cmake --install build-android --prefix win-gpu/ --config Release

# cmd execution

cd ..
adb push win-gpu/ /data/local/tmp/

# compression (skip)
tar -cf win-gpu.tar win-gpu
adb push win-gpu.tar /data/local/tmp/
adb shell
cd /data/local/tmp
tar -xf win-gpu.tar

chmod -R 755 win-gpu


```


# Mac Compile
```
# NDK Compile
cmake -DCMAKE_BUILD_TYPE=Release \
-DCMAKE_TOOLCHAIN_FILE=$HOME/android-sdk/ndk/26.3.11579264/build/cmake/android.toolchain.cmake \
-DOPENCL_ICD_LOADER_HEADERS_DIR=$HOME/android-sdk/ndk/26.3.11579264/toolchains/llvm/prebuilt/darwin-x86_64/sysroot/usr/include \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=24 \
-DANDROID_STL=c++_shared \
-B build_ndk26

cmake --build build_ndk26 --config Release -j 22

# llama.cpp compile
export ANDROID_NDK=~/android-sdk/ndk/26.3.11579264

cmake \
-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF \
-B build-android

## OpenCL Profiling

cmake \
-DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DCMAKE_CXX_FLAGS="-DGGML_OPENCL_PROFILING" \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF \
-B build-android

cmake --build build-android --config Release -j 22

mkdir OpenCL-Profiling

cmake --install build-android --prefix OpenCL-Profiling/ --config Release

adb push OpenCL-Profiling/ /data/local/tmp/
adb shell

cd /data/local/tmp/OpenCL-Profiling

LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 16
```

# Trigger mobile server to finish datasets latency

- mobile phone:

LD_LIBRARY_PATH=lib ./bin/llama-server -m ../models/deepseek-v2-lite-chat-q4_0.gguf -c 4096 --host 0.0.0.0 --port 8080

LD_LIBRARY_PATH=lib ./bin/llama-server -m ../models/deepseek-v2-lite-chat-q4_0.gguf -c 4096 --override-kv deepseek2.expert_used_count=int:4 --host 0.0.0.0 --port 8080

LD_LIBRARY_PATH=lib ./bin/llama-server -m ../models/deepseek-v2-lite-chat-q4_0.gguf -c 4096 --override-kv deepseek2.expert_used_count=int:2 --host 0.0.0.0 --port 8080

- computer

adb forward tcp:8080 tcp:8080
adb forward --remove tcp:8080

# GGML_OPENCL_PROFILING to profiling kernel launch
cmake \
-DCMAKE_TOOLCHAIN_FILE=$HOME/Sean/Hexagon_SDK/6.4.0.2/tools/android-ndk-r25c/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DCMAKE_CXX_FLAGS="-DGGML_OPENCL_PROFILING" \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF \
-B build-android

cmake --build build-android --config Release -j 22

LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 16
LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 32
LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 64
LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 128
LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 256
LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/deepseek-v2-lite-chat-q4_0.gguf -n 1 -no-cnv -f ../models/fix-token.txt --no-display-prompt --no-warmup -ngl 30 -ub 512

# GGML_TOKEN_STAT to profiling token-per-expert
cmake \
-DCMAKE_TOOLCHAIN_FILE=$HOME/Sean/Hexagon_SDK/6.4.0.2/tools/android-ndk-r25c/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DCMAKE_CXX_FLAGS="-DGGML_TOKEN_STAT" \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF \
-B build-android

cmake --build build-android --config Release -j 22

mkdir token-stat

cmake --install build-android --prefix token-stat/ --config Release

# Head Skip
./build/bin/llama-cli -m ../llama.cpp/models/deepseek-v2-lite-chat-q4_0.gguf --attn-heads 4 --override-kv deepseek2.expert_used_count=int:1 -f fix-token.txt -no-cnv --no-display-prompt -n 1

# Skip layer
./build/bin/llama-server -m ../llama.cpp/models/deepseek-v2-lite-chat-q4_0.gguf --attn-heads 0 -sl 27

# MoE-Offloading
cmake \
-DCMAKE_TOOLCHAIN_FILE=$HOME/Sean/Hexagon_SDK/6.4.0.2/tools/android-ndk-r25c/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DCMAKE_CXX_FLAGS="-DLLAMA_BACK_CPU" \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF \
-B build-android