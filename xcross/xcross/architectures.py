from typing import NamedTuple


class Architecture(NamedTuple):
    name: str
    triplet: str
    system_include_dirs: list[str]
    system_library_dirs: list[str]
    extra_definitions: list[str]


architectures = {
    "x64": Architecture(
        name="x64",
        triplet="x86_64-pc-windows-msvc",
        system_include_dirs=[
            "/xwin/crt/include",
            "/xwin/sdk/include/shared",
            "/xwin/sdk/include/ucrt",
            "/xwin/sdk/include/um",
        ],
        system_library_dirs=[
            "/xwin/crt/lib/x86_64",
            "/xwin/sdk/lib/ucrt/x86_64",
            "/xwin/sdk/lib/um/x86_64"
        ],
        extra_definitions=[],
    ),
    "armv7": Architecture(
        name="armv7",
        triplet="armv7-pc-windows-msvc",
        system_include_dirs=[
            "/xwin/crt/include",
            "/xwin/sdk/include/shared",
            "/xwin/sdk/include/ucrt",
            "/xwin/sdk/include/um",
        ],
        system_library_dirs=[
            "/xwin/crt/lib/aarch",
            "/xwin/sdk/lib/ucrt/aarch",
            "/xwin/sdk/lib/um/aarch"
        ],
        extra_definitions=["_ARM_WINAPI_PARTITION_DESKTOP_SDK_AVAILABLE"],
    ),
}
