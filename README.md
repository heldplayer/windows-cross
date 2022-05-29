# windows-cross

Repository containing tools and a Docker image for cross-compiling Windows apps from Linux using LLVM.

## Setup

The suggested usage is to use the Docker image to build programs.

In my case I set this up using VSCode with the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
I've then configured the `.devcontainer/devcontainer.json` file in this repository as follows:
```json
{
    "name": "Windows cross-compiling Environment",
    "build": {
        "dockerfile": "../Dockerfile"
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-vscode.cpptools",
                "ms-python.python"
            ],
            "settings": {
                "python.formatting.provider": "black",
                "python.formatting.blackArgs": [
                    "--line-length",
                    "119"
                ],
                "editor.rulers": [
                    120
                ],
                "explorer.autoReveal": false
            }
        }
    }
}
```

With that, if I open the repository in VSCode, I'll be prompted to reopen in a container, or if I dismiss that I can do so at a later point by clicking the "Open a Remote Window" button on the bottom left and selecting "Reopen in Container".

## Generating Ninja build directory

The `xcross-setup` script sets up a ninja build directory to be run in the Docker container.

```
usage: xcross-setup [-h] -t {x86_64,armv7} [-f] builddir [targets.yaml]

positional arguments:
  builddir              the target directory to build in.
  targets.yaml          the definition of compile targets.

options:
  -h, --help            show this help message and exit
  -t {x86_64,armv7}, --target-architecture {x86_64,armv7}
                        which architecture to create the build environment for.
  -f, --force           force creation of the environment even if builddir is not empty. WARNING: will empty the directory instead
```

The `targets.yaml` file defines the targets to build.
For now it's quite simple and only attempts to build executables, without support for static or dynamic libraries, or dependencies between targets.

After running this command, cd into the builddir and run `ninja` to build your program.
If you make a change to the `targets.yaml` file, you will need to delete the builddir and run `xcross-setup` again, or you can pass the `-f`/`--force` flag to overwrite the directory directly.

### Sample `targets.yaml`

The following is an example taken from the ["Your First Windows Program"](samples/first-windows-program) sample:
```yaml
targets:
  - name: LearnWindows
    system_libraries:
      - user32
    sources:
      - main.cpp
    compiler_definitions:
      - "WINVER=0x0603"  # Windows 8.1
      - "UNICODE"
    compiler_args:
      - "-std=c++11"
```

In this example:
- `name` is the target name
- `system_libraries` refers to the system libraries linked through `-l<lib>`
- `sources` contains all source C++ files to compile
- `compiler_definitions` contains a list of all compiler definitions
- `compiler_args` are some extra arguments given to the compiler

Additionally:
- `executable` can be set to explicitly set the executable name, otherwise it defaults to appending `.exe` to the end of the target
- `linker_args` can be set to give extra arguments to the linker

## Samples

The following samples exist:
- ["Your First Windows Program"](samples/first-windows-program): Simplest functioning Win32 app.
- ["COM Interface"](samples/com-interface): Folder containing COM Interface samples (only 1 currently).
- ["Direct2D"](samples/direct2d): Sample containing Direct2D rendering code.
- ["Frame Extension"](samples/frame-extend): Sample that extends the client area into the window frame.

## Why all this effort?
Good question!

I tried using CMake at first to cross-compile, however I had mixed success as it would kind of work on CMake 3.18, but required me running cmake a 2nd time before being able to actually compile and CMake appending the appropriate extensions to its targets.
On higher versions of CMake I couldn't get it to compile at all.

I also attempted Meson, and while this worked fine enough, I got annoyed at the fact that its documentation is not easy to go through, and that there's seemingly no way to disable some default compiler and linker arguments from being passed. As well as the requirement to tell the linker specifically what subsystem to compile for even though it can figure this out on its own as well.

So, knowing the required arguments to give to the compiler and linker, and having a good enough idea of Ninja, I just decided to write my own thing for my very niche use case rather than giving myself a headache over trying to get build systems to conform to my requirements.
