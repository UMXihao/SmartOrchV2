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

$ mkdir install

$ cmake --build build-android --config Release -j 22

$ cmake --install build-android --prefix install/ --config Release

$ adb push install /data/local/tmp/smartorchv2/

$ LD_LIBRARY_PATH=lib ./bin/llama-cli -m ../{model}.gguf -n {output-length} -no-cnv -p "{your-prompt}" --no-display-prompt -ngl 30 -c 6000
```


## Access the server started on the mobile phone from the computer.

- mobile phone:

    LD_LIBRARY_PATH=lib ./bin/llama-server -m {model}.gguf --host 0.0.0.0 --port 8080

- computer
  
    adb forward tcp:8080 tcp:8080