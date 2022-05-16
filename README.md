# windows-cross

Repository containing tools for cross-compiling Windows apps from Linux using LLVM.

## Using the ninja configuration generator

The `build_setup.py` file sets up a ninja build script to be run in the Docker container.

```
usage: build_setup.py [-h] -t {x86_64,armv7} [-f] builddir [targets.yaml]

positional arguments:
  builddir              the target directory to build in.
  targets.yaml          the definition of compile targets.

optional arguments:
  -h, --help            show this help message and exit
  -t {x86_64,armv7}, --target-architecture {x86_64,armv7}
                        which architecture to create the build environment for.
  -f, --force           force creation of the environment even if builddir is not empty. WARNING: will empty the directory instead!
```

The `targets.yaml` file defines the targets to build.
For now it's quite simple and only attempts to build executables, without support for static or dynamic libraries, or dependencies between targets.

The following is an example taken from the "Your First Windows Program" sample:
```yaml
targets:
  - name: LearnWindows
    system_libraries:
      - user32
    sources:
      - main.cpp
    compiler_definitions:
      - "WINVER=0x0603"  # Windows 8.1
```

In this example:
- `name` is the target name
- `system_libraries` refers to the system libraries linked through `-l<lib>`
- `sources` contains all source C++ files to compile
- `compiler_definitions` contains a list of all compiler definitions

Additionally, `executable` can be set to explicitly set the executable name, otherwise it defaults to appending `.exe` to the end of the target.

## Combining it all

First build the Docker container from the [base image](https://github.com/heldplayer/windows-cross-base), then run `./make_venv.sh` to create a virtual environment with Ninja and pyyaml installed.
Next, go to the code you want to compile and either make your `targets.yaml` file or go to one that already has it and run `build_setup.py` (for example: `build_setup.py -t x86_64 build`) (note that `build_setup.py` has been added as an executable in the virtual environment for easy use.)
Finally, run the Ninja script in the Docker container, for example:
```bash
docker run --rm -it -v $(pwd):/data cross bash -c "cd build ; ninja -v"
```
This will change into the build directory and run Ninja while also keeping access to the actual source files in the folder above.

## Samples

The following samples exist:
- ["Your First Windows Program"](samples/first-windows-program): simple 1 source file, 1 executable output.

## Why all this effort?
Good question!

I tried using CMake at first to cross-compile, however I had mixed success as it would kind of work on CMake 3.18, but required me running cmake a 2nd time before being able to actually compile and CMake appending the appropriate extensions to its targets.
On higher versions of CMake I couldn't get it to compile at all.

I also attempted Meson, and while this worked fine enough, I got annoyed at the fact that its documentation is not easy to go through, and that there's seemingly no way to disable some default compiler and linker arguments from being passed. As well as the requirement to tell the linker specifically what subsystem to compile for even though it can figure this out on its own as well.

So, knowing the required arguments to give to the compiler and linker, and having a good enough idea of Ninja, I just decided to write my own thing for my very niche use case rather than giving myself a headache over trying to get build systems to conform to my requirements.
