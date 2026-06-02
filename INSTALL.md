# Installation Guide - mcnptoolspro

This guide explains how to build and install `mcnptoolspro` for development.

## Windows

### Prerequisites

Install these first:

1. Python 3.7 or newer
2. CMake 3.21 or newer
3. Git
4. Visual Studio 2017 or newer, with the "Desktop development with C++" workload

HDF5 is handled by `install_dev.py` on Windows. If the script cannot find a
local vcpkg installation with `hdf5:x64-windows`, it will:

1. clone vcpkg next to this repository, for example `C:\Users\<you>\SOFTWARES\vcpkg`
2. bootstrap vcpkg
3. install `hdf5:x64-windows`
4. configure CMake with explicit HDF5 and ZLIB paths

The script intentionally does not use `CMAKE_TOOLCHAIN_FILE` for vcpkg because
the `shacl-F5_CXX` dependency wraps `find_package()`, which can recurse through
the vcpkg HDF5 wrapper.

### Install

```powershell
git clone https://github.com/quentinducasse/mcnptoolspro.git
cd mcnptoolspro
python install_dev.py
```

That single command configures CMake, builds the Python extension, copies the
required runtime DLLs, creates an editable Python install, and verifies the
installation.

### What Gets Copied

On Windows, the package directory receives:

- `_mcnptools_wrap.pyd`
- `hdf5.dll`
- `z.dll`
- `aec.dll`
- `szip.dll`

These DLLs must sit beside the `.pyd` so Python can load the extension reliably.

## Linux

Install the system HDF5 development package first:

```bash
sudo apt update
sudo apt install build-essential git python3-dev libhdf5-dev cmake
python3 install_dev.py
```

For Fedora/RedHat:

```bash
sudo yum install gcc-c++ git python3-devel hdf5-devel cmake
python3 install_dev.py
```

For Arch Linux:

```bash
sudo pacman -S base-devel git python hdf5 cmake
python install_dev.py
```

## macOS

Install prerequisites with Homebrew:

```bash
brew install hdf5 cmake python git
python3 install_dev.py
```

## Verify

After installation:

```bash
python -c "import mcnptoolspro as m; print(m.__file__); print(m.Ptrac.HDF5_PTRAC)"
```

Expected result: the import succeeds and `HDF5_PTRAC` prints `2`.

## Troubleshooting

### VS Code Shows a Yellow Underline on `import mcnptoolspro`

This is usually a Pylance/static-analysis issue, not an installation failure.
Make sure VS Code uses the same Python interpreter that ran `install_dev.py`.

This repository includes a workspace setting that adds `./python` to
`python.analysis.extraPaths`. If the underline remains, reload VS Code:

```text
Ctrl+Shift+P -> Developer: Reload Window
```

### Windows: HDF5 Not Found

Run:

```powershell
python install_dev.py
```

The script should install HDF5 through vcpkg automatically. If it fails, check
that Git, CMake, and Visual Studio C++ tools are available in your environment.

### Windows: DLL Load Failed

Re-run:

```powershell
python install_dev.py
```

The script recopies the required DLLs next to `_mcnptools_wrap.pyd`.

### CMake Cache Problems

The installer clears stale CMake cache files in `build` before configuring. If
you manually experimented with other CMake settings, remove the build directory
and run the installer again:

```powershell
Remove-Item build -Recurse -Force
python install_dev.py
```

## Notes for Developers

- `build` is the canonical CMake build directory.
- `build_hdf5manual` was only a temporary manual workaround and is not required.
- Python code changes are picked up immediately through the editable install.
- C++ changes require re-running `python install_dev.py` or rebuilding the
  `_mcnptools_wrap` target.
