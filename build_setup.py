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

ARCHITECTURES = ['x86_64', 'armv7']
TARGET_TRIPLETS = {
    'x86_64': 'x86_64-pc-windows-msvc',
    'armv7': 'armv7-pc-windows-msvc',
}
INCLUDE_DIRS = {
    'x86_64': ['/xwin/crt/include', '/xwin/sdk/include/shared', '/xwin/sdk/include/ucrt', '/xwin/sdk/include/um'],
    'armv7': ['/xwin/crt/include', '/xwin/sdk/include/shared', '/xwin/sdk/include/ucrt', '/xwin/sdk/include/um'],
}
LIBRARY_DIRS = {
    'x86_64': ['/xwin/crt/lib/x86_64', '/xwin/sdk/lib/ucrt/x86_64', '/xwin/sdk/lib/um/x86_64'],
    'armv7': ['/xwin/crt/lib/aarch', '/xwin/sdk/lib/ucrt/aarch', '/xwin/sdk/lib/um/aarch'],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('build_dir', metavar='builddir',
                        help='the target directory to build in.')
    parser.add_argument('targets', metavar='targets.yaml', nargs='?', default='targets.yaml',
                        help='the definition of compile targets.')
    parser.add_argument('-t', '--target-architecture', dest='architecture', choices=ARCHITECTURES, required=True,
                        help='which architecture to create the build environment for.')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='force creation of the environment even if builddir is not empty.\n'
                             'WARNING: will empty the directory instead!')

    arguments = parser.parse_args()

    build_dir = arguments.build_dir
    targets_file = arguments.targets
    architecture = arguments.architecture
    triplet = TARGET_TRIPLETS[architecture]
    include_dirs = INCLUDE_DIRS[architecture]
    library_dirs = LIBRARY_DIRS[architecture]

    with open(targets_file, 'r') as f:
        try:
            targets_data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    targets = [TargetDefinition(target) for target in targets_data['targets']]

    p = Path(build_dir)

    if p.exists():
        if not arguments.force:
            parser.error('builddir already exists')

        if not p.is_dir():
            parser.error('builddir already exists but is not a directory, not proceeding')

        for path in p.glob('*'):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    else:
        p.mkdir()

    build_file_path = p / 'build.ninja'

    print(targets)

    with open(build_file_path, 'w') as f:
        f.write('# Automatically generated file by an unnamed tool for cross-compiling from Linux to Windows\n\n')

        # Paths
        f.write('SYSTEM_INCLUDE_DIRS = ' + ' '.join(f'-isystem {f}' for f in include_dirs) + '\n')
        f.write('SYSTEM_LIBRARY_DIRS = ' + ' '.join(f'-L{f}' for f in library_dirs) + '\n')
        f.write('\n')

        # C++ compiler
        f.write('rule CXX_COMPILER\n')
        f.write(f'  command = clang++ --target={triplet} $ARGS -fuse-ld=lld -o $out -c $in\n')
        f.write('  description = Compiling C++ object $out\n')
        f.write('\n')

        # C++ linker
        f.write('rule CXX_LINKER\n')
        f.write(f'  command = clang++ --target={triplet} $LINK_ARGS -fuse-ld=lld -o $out $in\n')
        f.write('  description = Linking $out\n')
        f.write('\n')

        f.write('\n')

        for target in targets:
            workdir = target.name + '.dir'
            obj_files = []

            for source in target.sources:
                obj = f'{workdir}/{source}.o'
                obj_files.append(obj)

                f.write(f'build {obj}: CXX_COMPILER ../{source}\n')
                f.write('  ARGS = $SYSTEM_INCLUDE_DIRS -std=c++11\n')
                f.write('\n')

            f.write(f'build {target.executable}: CXX_LINKER {" ".join(obj_files)}\n')
            f.write(f'  LINK_ARGS = $SYSTEM_LIBRARY_DIRS {" ".join(f"-l{lib}" for lib in target.system_libraries)}\n')
            f.write('\n')

        f.write(f'build all: phony {" ".join(target.executable for target in targets)}\n')
        f.write('default all\n')


class TargetDefinition:
    def __init__(self, data):
        print(data)
        self.name = data['name']
        self.executable = data.get('executable', self.name + '.exe')
        self.system_libraries = data.get('system_libraries', [])
        self.sources = data.get('sources', [])
        self.definitions = data.get('compiler_definitions', [])

    def __repr__(self):
        return f'TargetDefinition(name={self.name!r}, executable={self.executable!r}, ' \
               f'system_libraries={self.system_libraries!r}, sources={self.sources!r}, ' \
               f'compiler_definitions={self.definitions!r})'


if __name__ == '__main__':
    main()
