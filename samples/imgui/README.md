# Frame Extension

This sample is based on Dear ImGui example for Win32 on D3D9 found at https://github.com/ocornut/imgui/tree/master/examples/example_win32_directx9

Note that no files are present here as it would require importing the entire functional source code of Dear ImGui.
Instead if you would like to try this sample, download the repository and manually copy over the required files (and possibly update `targets.yaml` in case it's no longer valid).

Note also that this sample requires some special handling for compiling to ARMv7, as LLVM currently does not support exception handling for Windows on aarch, hence the `-fno-exceptions` compiler argument. ([see here](https://github.com/llvm/llvm-project/issues/37689))

Additionally, there is a required definition `_CRT_USE_BUILTIN_OFFSETOF` to make `offsetof` be `constexpr`.
The reason is the following snippet from `stddef.h` in the Windows Universal C Runtime (ucrt):
```cpp
#if defined(_MSC_VER) && !defined(_CRT_USE_BUILTIN_OFFSETOF)
    #ifdef __cplusplus
        #define offsetof(s,m) ((size_t)&reinterpret_cast<char const volatile&>((((s*)0)->m)))
    #else
        #define offsetof(s,m) ((size_t)&(((s*)0)->m))
    #endif
#else
    #define offsetof(s,m) __builtin_offsetof(s,m)
#endif
```
