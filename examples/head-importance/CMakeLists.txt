# examples/head-importance/CMakeLists.txt

set(TARGET llama-head-importance)

add_executable(${TARGET}
        head-importance.cpp
)

target_link_libraries(${TARGET}
        PRIVATE
        common
        llama
        ggml
)