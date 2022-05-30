from __future__ import annotations


class TargetBase:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.system_libraries = data.get("system_libraries", [])
        self.sources = data.get("sources", [])
        self.definitions = data.get("compiler_definitions", [])
        self.compiler_args = data.get("compiler_args", [])
        self.linker_args = data.get("linker_args", [])

    def _get_repr_parts(self):
        return [
            ("name", repr(self.name)),
            ("system_libraries", repr(self.system_libraries)),
            ("sources", repr(self.sources)),
            ("definitions", repr(self.definitions)),
            ("compiler_args", repr(self.compiler_args)),
            ("linker_args", repr(self.linker_args)),
        ]

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join('='.join(p) for p in self._get_repr_parts())})"


class TargetExecutable(TargetBase):
    def __init__(self, data: dict):
        super().__init__(data)
        self.executable_file = data.get("executable_file", self.name + ".exe")

    def _get_repr_parts(self):
        return super()._get_repr_parts() + [
            ("executable_file", repr(self.executable_file)),
        ]


class TargetSharedLibrary(TargetBase):
    def __init__(self, data: dict):
        super().__init__(data)
        self.library_file = data.get("library_file", self.name + ".dll")

    def _get_repr_parts(self):
        return super()._get_repr_parts() + [
            ("library_file", repr(self.library_file)),
        ]


class TargetStaticLibrary(TargetBase):
    def __init__(self, data: dict):
        super().__init__(data)
        self.library_file = data.get("library_file", self.name + ".lib")

    def _get_repr_parts(self):
        return super()._get_repr_parts() + [
            ("library_file", repr(self.library_file)),
        ]


target_names = {
    "executable": TargetExecutable,
    "shared library": TargetSharedLibrary,
    "static library": TargetStaticLibrary,
}


def target_desc_to_object(data: dict) -> TargetBase:
    if "name" not in data:
        raise ValueError("Missing name for target")
    if "type" not in data:
        raise ValueError("Missing type for target")

    if data["type"] not in target_names:
        raise ValueError(f"Unknown target type {data['type']!r}")

    return target_names[data["type"]](data)
