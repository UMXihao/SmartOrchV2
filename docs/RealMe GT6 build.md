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

mkdir build-android && cd build-android

$ cmake .. \
-DCMAKE_TOOLCHAIN_FILE=$HOME/Sean/Hexagon_SDK/6.4.0.2/tools/android-ndk-r25c/build/cmake/android.toolchain.cmake \
-DANDROID_ABI=arm64-v8a \
-DANDROID_PLATFORM=android-28 \
-DBUILD_SHARED_LIBS=OFF \
-DLLAMA_CURL=OFF \
-DGGML_OPENCL=ON \
-DGGML_OPENMP=OFF 

$ cd ..

$ mkdir smartorch-gpu

$ cmake --build build-android --config Release -j 22

$ cmake --install build-android --prefix smartorch-gpu/ --config Release

$ adb push smartorch-gpu /data/local/tmp/

$ LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../models/{model}.gguf -n {output-length} -no-cnv -p "{your-prompt}" --no-display-prompt -ngl 30 -c 6000
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
