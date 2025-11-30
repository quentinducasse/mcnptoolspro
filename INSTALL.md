# Installation Guide - mcnptoolspro

**Multiple installation methods for all use cases**

---

## 📦 Quick Install (Recommended)

### From GitHub (no clone needed)

```bash
pip install git+https://github.com/quentinducasse/mcnptoolspro.git#subdirectory=python
```

**Note**: The `#subdirectory=python` part is required because `setup.py` is located in the `python/` directory.

**That's it!** You can now use:

```python
import mcnptoolspro as m
ptrac = m.Ptrac('file.ptrac', m.Ptrac.ASC_PTRAC)
```

---

## 🔧 Install from Source (Advanced)

If you want to **modify the code** or **contribute**, install from source:

### 1️⃣ Clone the repository

```bash
git clone https://github.com/quentinducasse/mcnptoolspro.git
cd mcnptoolspro
```

### 2️⃣ Install (choose one method)

#### **Method A: Direct pip install** (standard)

```bash
cd python
pip install .
```

#### **Method B: Editable install** (for development)

```bash
cd python
pip install -e .
```

With `-e`, changes to Python code are immediately active (no reinstall needed).

---

## 🛠️ Manual Build (Expert Mode)

For **maximum control** or if pip install fails, build manually:

### Windows

**Prerequisites** (install these BEFORE building):

1. ✅ **Visual Studio 2017 or later** (with "Desktop development with C++" workload)
   - Download: https://visualstudio.microsoft.com/downloads/
   - **OR** install "Build Tools for Visual Studio" (smaller, CLI-only)
   - **Required** for MSVC compiler (CMake won't work without it!)

2. ✅ **CMake 3.13+**
   - Install via: `choco install cmake` (Chocolatey)
   - **OR** download from: https://cmake.org/download/
   - **OR** install via pip: `pip install cmake`

3. ✅ **Python 3.7+**
   - Download from: https://python.org
   - **OR** install from Microsoft Store

Once prerequisites are installed, follow these build steps:

```powershell
# 1. Configure CMake (skip tests to avoid gtest errors)
cmake -S . -B build -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF

# 2. Build the Python wrapper
cmake --build build --config Release --target _mcnptools_wrap -j 8

# 3. Copy the compiled wrapper
Copy-Item build\python\mcnptoolspro\Release\_mcnptools_wrap.pyd python\mcnptoolspro\

# 4. Install the Python package
cd python
pip install -e .
```

**Notes**:
- ✅ `hdf5.dll` is **already bundled** in the repository (in `python/mcnptoolspro/`)
- ✅ No need to install HDF5 separately on Windows!
- The DLL is automatically included when you clone the repo

**Important**: If switching between installation methods (manual build, pip install, etc.), remove `build/CMakeCache.txt` to avoid CMake configuration conflicts:

```powershell
# Windows
Remove-Item build\CMakeCache.txt -ErrorAction SilentlyContinue

# Linux/macOS
rm -f build/CMakeCache.txt
```

### Linux / macOS

**Prerequisite**: Install HDF5 using your system package manager:

```bash
# Ubuntu/Debian
sudo apt-get install libhdf5-dev

# Fedora/RedHat
sudo yum install hdf5-devel

# Arch Linux
sudo pacman -S hdf5

# macOS (Homebrew)
brew install hdf5
```

Then build mcnptoolspro:

```bash
# 1. Configure CMake
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release

# 2. Build the Python wrapper
cmake --build build --target _mcnptools_wrap -j $(nproc)

# 3. Copy the compiled wrapper
cp build/python/mcnptoolspro/_mcnptools_wrap.so python/mcnptoolspro/

# 4. Install the Python package
cd python
pip install -e .
```

**Note**: Unlike Windows, HDF5 is **not bundled** on Linux/macOS. You must install it via your package manager (it's fast and standard practice for C++ projects).

---

## 📋 Requirements

### System Requirements

| Platform | Requirements |
|----------|-------------|
| **Windows** | Visual Studio 2017+ (MSVC), CMake 3.13+, Python 3.7+ *(HDF5 bundled!)* |
| **Linux** | GCC 7+, CMake 3.13+, Python 3.7+, libhdf5-dev |
| **macOS** | Xcode Command Line Tools, CMake 3.13+, Python 3.7+ |

### Python Dependencies

**None!** mcnptoolspro has no Python dependencies (pure C++ wrapper).

### HDF5 Dependency

| Platform | HDF5 Installation |
|----------|-------------------|
| **Windows** | ✅ **Bundled** - `hdf5.dll` included in repository |
| **Linux** | ⚙️ **System package** - `sudo apt install libhdf5-dev` (or equivalent) |
| **macOS** | ⚙️ **Homebrew** - `brew install hdf5` |

**Why bundled on Windows only?**
- Windows: DLL files are portable and self-contained
- Linux/macOS: Shared libraries (`.so`/`.dylib`) are distribution-specific and should come from the system package manager (standard practice)

---

## ✅ Verify Installation

After installation, test that it works:

```bash
python -c "import mcnptoolspro; print('mcnptoolspro installed successfully')"
```

**Expected output**: `mcnptoolspro installed successfully`

---

## 🐳 Docker Installation

Use mcnptoolspro in a Docker container:

### Quick test

```bash
docker run -it --rm python:3.9-slim bash -c "
  apt-get update && apt-get install -y build-essential cmake g++ git && \
  pip install git+https://github.com/quentinducasse/mcnptoolspro.git#subdirectory=python && \
  python -c 'import mcnptoolspro; print(\"OK\")'
"
```

### Production Dockerfile

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    git \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Install mcnptoolspro
RUN pip install --no-cache-dir git+https://github.com/quentinducasse/mcnptoolspro.git#subdirectory=python

# Verify installation
RUN python -c "import mcnptoolspro; print('mcnptoolspro installed')"

# Your application
WORKDIR /app
COPY . /app

CMD ["python", "your_app.py"]
```

Build and run:

```bash
docker build -t myapp .
docker run -it --rm myapp
```

---

## 🔄 Update mcnptoolspro

### If installed from GitHub

```bash
pip install --upgrade git+https://github.com/quentinducasse/mcnptoolspro.git#subdirectory=python
```

### If installed from source (editable)

```bash
cd mcnptoolspro
git pull origin main

# Rebuild if C++ code changed
cmake --build build --config Release --target _mcnptools_wrap
cp build/python/mcnptoolspro/Release/_mcnptools_wrap.pyd python/mcnptoolspro/  # Windows
# OR
cp build/python/mcnptoolspro/_mcnptools_wrap.so python/mcnptoolspro/  # Linux/macOS
```

---

## 🐛 Troubleshooting

### Issue: `CMake not found`

**Solution**: Install CMake

```bash
# Windows (via Chocolatey)
choco install cmake

# Linux
sudo apt-get install cmake  # Debian/Ubuntu
sudo yum install cmake       # RedHat/CentOS

# macOS
brew install cmake

# OR via pip
pip install cmake
```

---

### Issue: `Visual Studio not found` (Windows)

**Solution**: Install Visual Studio 2017 or later

Download from: https://visualstudio.microsoft.com/downloads/

Choose "Desktop development with C++" workload.

---

### Issue: `libhdf5 not found` (Linux)

**Solution**: Install HDF5 development libraries

```bash
# Debian/Ubuntu
sudo apt-get install libhdf5-dev

# RedHat/CentOS
sudo yum install hdf5-devel

# Arch Linux
sudo pacman -S hdf5
```

---

### Issue: `ImportError: DLL load failed` (Windows)

**Note**: `hdf5.dll` is now **bundled** in the repository, so this should rarely happen!

**If it still occurs**, possible solutions:

1. **Verify hdf5.dll is present**:
   ```powershell
   ls python\mcnptoolspro\hdf5.dll
   ```
   If missing, the file should be in the repo after `git clone`. Try re-cloning.

2. **Missing Visual C++ runtime**: Download and install:
   - [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

### Issue: `error: Unable to find a compatible Visual Studio installation`

**Solution**: Ensure Visual Studio is in PATH

```powershell
# Check if MSBuild is available
where msbuild

# If not found, run this in Visual Studio Developer Command Prompt
# OR install "Build Tools for Visual Studio"
```

---

### Issue: Build succeeds but `import mcnptoolspro` fails

**Solution**: Wrapper not copied to package

```bash
# Windows
Copy-Item build\python\mcnptoolspro\Release\_mcnptools_wrap.pyd python\mcnptoolspro\ -Force

# Linux/macOS
cp build/python/mcnptoolspro/_mcnptools_wrap.so python/mcnptoolspro/
```

Then retry:

```bash
cd python
pip install --force-reinstall -e .
```

---

### Issue: `ModuleNotFoundError: No module named 'mcnptoolspro'`

**Solution**: Installation failed or wrong Python environment

```bash
# Check where Python looks for packages
python -c "import sys; print('\n'.join(sys.path))"

# Check if mcnptoolspro is installed
pip list | grep mcnptools

# If not listed, reinstall
pip install --force-reinstall git+https://github.com/quentinducasse/mcnptoolspro.git
```

---

### Issue: Permission denied during `pip install`

**Solution**: Install in user directory

```bash
# Add --user flag
pip install --user git+https://github.com/quentinducasse/mcnptoolspro.git
```

---

### Issue: VSCode shows yellow/orange underline on `import mcnptoolspro`

**Cause**: VSCode/Pylance can't find the package or is using a different Python interpreter.

**Solution**:

1. **Select the correct Python interpreter**:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type: `Python: Select Interpreter`
   - Choose the Python interpreter where mcnptoolspro is installed
   - Verify with: `python -c "import mcnptoolspro; print(mcnptoolspro.__file__)"`

2. **Reload VSCode window**:
   - Press `Ctrl+Shift+P`
   - Type: `Developer: Reload Window`

3. **Check installation**:
   ```bash
   # Verify mcnptoolspro is installed
   pip list | grep mcnptools

   # Test import works
   python -c "import mcnptoolspro; print('OK')"
   ```

**Note**: The yellow underline is just a warning from the static analyzer. If `python -c "import mcnptoolspro"` works in the terminal, the package is correctly installed and will work at runtime.

---

### Issue: CMake configuration conflict when switching installation methods

**Cause**: CMake cache from a previous build method causes conflicts.

**Solution**: Remove the CMake cache file:

```powershell
# Windows
Remove-Item build\CMakeCache.txt -ErrorAction SilentlyContinue

# Linux/macOS
rm -f build/CMakeCache.txt
```

Then retry the installation.

---

## 🧪 Test Installation

### Quick test

```python
import mcnptoolspro as m
print(f"mcnptoolspro loaded from: {m.__file__}")
```

### Full test (if you have PTRAC files)

```python
import mcnptoolspro as m

# Read PTRAC file
ptrac = m.Ptrac('your_file.ptrac', m.Ptrac.ASC_PTRAC)

# Read first 10 histories
histories = ptrac.ReadHistories(10)

# Print summary
print(f"Read {len(histories)} histories")
for i, hist in enumerate(histories):
    print(f"  History {i+1}: {hist.GetNumEvents()} events")
```

---

## 📦 Installation in Virtual Environment (Recommended)

### Using venv (Python 3.3+)

```bash
# Create virtual environment
python -m venv mcnptools_env

# Activate (Windows)
mcnptools_env\Scripts\activate

# Activate (Linux/macOS)
source mcnptools_env/bin/activate

# Install mcnptoolspro
pip install git+https://github.com/quentinducasse/mcnptoolspro.git

# Use it
python your_script.py

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n mcnptools python=3.9

# Activate
conda activate mcnptools

# Install mcnptoolspro
pip install git+https://github.com/quentinducasse/mcnptoolspro.git

# Use it
python your_script.py

# Deactivate when done
conda deactivate
```

---

## 🔐 Offline Installation

If you need to install on a machine **without internet access**:

### 1. On a machine WITH internet:

```bash
# Clone the repository
git clone https://github.com/quentinducasse/mcnptoolspro.git

# Create a tarball
tar -czf mcnptoolspro.tar.gz mcnptoolspro/
```

### 2. Transfer `mcnptoolspro.tar.gz` to offline machine

### 3. On the offline machine:

```bash
# Extract
tar -xzf mcnptoolspro.tar.gz
cd mcnptoolspro

# Install
pip install .
```

---

## 📊 Installation Options Summary

| Method | Command | Use Case |
|--------|---------|----------|
| **Quick** | `pip install git+https://...` | Normal users |
| **From source** | `pip install .` | Contributors, custom builds |
| **Editable** | `pip install -e .` | Active development |
| **Manual build** | `cmake + pip` | Debugging, expert control |
| **Docker** | `docker build ...` | Containerized deployment |
| **Offline** | `tar.gz + pip install .` | Air-gapped systems |

---

## 🆘 Still Having Issues?

1. **Check the docs**: [README.md](README.md)
2. **Read troubleshooting**: [BUILD_AND_DOCKER_GUIDE.md](BUILD_AND_DOCKER_GUIDE.md)
3. **Open an issue**: https://github.com/quentinducasse/mcnptoolspro/issues

Include in your issue:
- Operating system (Windows/Linux/macOS)
- Python version (`python --version`)
- CMake version (`cmake --version`)
- Full error message
- Installation method attempted

---

## ✅ Quick Checklist

After installation, verify:

- [ ] `import mcnptoolspro` works
- [ ] No error messages
- [ ] Can create `Ptrac` object
- [ ] Can read a PTRAC file (if you have one)

---

**Happy PTRAC parsing!** 🚀

---

**Documentation**: [README.md](README.md) | [Modifications](MODIFICATIONS_MCNPTOOLS_TO_MCNPTOOLSPRO.md) | [Build Guide](BUILD_AND_DOCKER_GUIDE.md)

**Support**: https://github.com/quentinducasse/mcnptoolspro/issues
