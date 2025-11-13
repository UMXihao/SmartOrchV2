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
$ mkdir install
$ cmake --build build-android --config Release -j 8
$ cmake --install build-android --prefix install/ --config Release
```

After installing, go ahead and download the model of your choice to your host system. Then:


```
$ adb shell "mkdir /data/local/tmp/smartorchv2"
$ adb push install /data/local/tmp/smartorchv2/
$ adb push {model}.gguf /data/local/tmp/smartorchv2/
$ adb shell
```

In the `adb shell`:

```
$ cd /data/local/tmp/smartorchv2/install
$ LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../{model}.gguf -n {output-length} -no-cnv -p "{your-prompt}"
```

