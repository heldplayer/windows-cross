#!/usr/bin/env python3

"""
This file is used to create a working ninja file for building Windows applications.

Instead of using CMake or Meson, a Python file is used because more high-level build tools always decide on their own
what options are passed to the compiler and linker.
"""

import argparse
import shutil
import yaml

from pathlib import Path

from xcross.targets import target_desc_to_object
from xcross.architectures import architectures
from xcross.compilers import CompilerCpp
from xcross.linkers import LinkerCpp


def main():
    # fmt: off
    parser = argparse.ArgumentParser(prog="xcross-setup")
    parser.add_argument("build_dir", metavar="builddir",
                        help="the target directory to build in.")
    parser.add_argument("targets", metavar="targets.yaml", nargs="?", default="targets.yaml",
                        help="the definition of compile targets.")
    parser.add_argument("-t", "--target-architecture", dest="architecture", choices=architectures.keys(), required=True,
                        help="which architecture to create the build environment for.")
    parser.add_argument("-f", "--force", dest="force", action="store_true",
                        help="force creation of the environment even if builddir is not empty.\n"
                             "WARNING: will empty the directory instead!")
    # fmt: on

    arguments = parser.parse_args()

    build_dir = arguments.build_dir
    targets_file = arguments.targets
    architecture = architectures[arguments.architecture]
    triplet = architecture.triplet
    extra_definitions = architecture.extra_definitions
    include_dirs = architecture.system_include_dirs
    library_dirs = architecture.system_library_dirs

    with open(targets_file, "r") as f:
        try:
            targets_data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    targets = [target_desc_to_object(target) for target in targets_data["targets"]]

    p = Path(build_dir)

    if p.exists():
        if not arguments.force:
            parser.error("builddir already exists")

        if not p.is_dir():
            parser.error("builddir already exists but is not a directory, not proceeding")

        for path in p.glob("*"):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    else:
        p.mkdir()

    build_file_path = p / "build.ninja"

    print(targets)

    with open(build_file_path, "w") as f:
        f.write("# Automatically generated file by an unnamed tool for cross-compiling from Linux to Windows\n\n")

        # Paths
        f.write("SYSTEM_INCLUDE_DIRS = " + " ".join(f"-isystem {f}" for f in include_dirs) + "\n")
        f.write("SYSTEM_LIBRARY_DIRS = " + " ".join(f"-L{f}" for f in library_dirs) + "\n")
        f.write("\n")

        # C++ compiler
        f.write("rule CXX_COMPILER\n")
        f.write(CompilerCpp.get_rule_contents(architecture))
        f.write("\n\n")

        # C++ linker
        f.write("rule CXX_LINKER\n")
        f.write(LinkerCpp.get_rule_contents(architecture))
        f.write("\n\n")

        f.write("\n")

        # Targets
        for target in targets:
            workdir = target.name + ".dir"
            obj_files = []

            definitions = " ".join(f"-D {definition}" for definition in extra_definitions + target.definitions)
            libraries = " ".join(f"-l{lib}" for lib in target.system_libraries)

            compiler_args = " ".join(target.compiler_args)
            linker_args = " ".join(target.linker_args)

            # Source files to object files
            for source in target.sources:
                obj = f"{workdir}/{source}.o"
                obj_files.append(obj)

                f.write(f"build {obj}: CXX_COMPILER ../{source}\n")
                f.write(f"  ARGS = $SYSTEM_INCLUDE_DIRS {definitions} {compiler_args} \n")
                f.write("\n")

            # Object files to executable
            f.write(f"build {target.executable_file}: CXX_LINKER {' '.join(obj_files)}\n")
            f.write(f"  LINK_ARGS = $SYSTEM_LIBRARY_DIRS {libraries} {linker_args}\n")
            f.write("\n")

        f.write(f"build all: phony {' '.join(target.executable_file for target in targets)}\n")
        f.write("default all\n")


if __name__ == "__main__":
    main()
