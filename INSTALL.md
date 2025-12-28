# Installation Guide - mcnptoolspro

**Platform-specific installation instructions**

---

## 📑 Table of Contents

- [Windows Installation](#-windows-installation)
- [Linux/macOS Installation](#-linuxmacos-installation)
- [Troubleshooting](#-troubleshooting)
- [Testing](#-test-installation)

---

## 🪟 Windows Installation

### Prerequisites

Install these tools **before** building mcnptoolspro:

1. **Visual Studio 2017 or later** (with "Desktop development with C++" workload)
   - Download: https://visualstudio.microsoft.com/downloads/
   - **OR** install "Build Tools for Visual Studio" (smaller, CLI-only)
   - **Required** for MSVC compiler (CMake won't work without it!)

2. **CMake 3.13+**
   - Install via: `choco install cmake` (Chocolatey)
   - **OR** download from: https://cmake.org/download/
   - **OR** install via pip: `pip install cmake`

3. **Python 3.7+**
   - Download from: https://python.org
   - **OR** install from Microsoft Store

4. **Git** (for cloning)
   - Download from: https://git-scm.com/

**Note**: `hdf5.dll` is **already bundled** in the repository. No need to install HDF5 separately on Windows!

### Installation Steps

```powershell
# 1. Clone the repository
git clone https://github.com/quentinducasse/mcnptoolspro.git
cd mcnptoolspro

# 2. Run the automated installation script
python install_dev.py
```

**What the script does:**
- ✓ Checks all prerequisites (Python, CMake, Git, Visual Studio)
- ✓ Configures CMake with Visual Studio generator
- ✓ Builds the C++ wrapper (`_mcnptools_wrap.pyd`)
- ✓ Copies the compiled wrapper to the Python package
- ✓ Installs the package in editable mode
- ✓ Verifies the installation works

That's it! The script handles everything automatically.

### Updating (Windows)

To update to the latest version:

```powershell
cd mcnptoolspro
git pull origin main

# Re-run the installation script
python install_dev.py
```

**Note**: Python code changes are picked up automatically (editable mode), but C++ changes require rebuilding.

---

## 🐧 Linux/macOS Installation

### Prerequisites

Install required tools and libraries:

#### Ubuntu/Debian

```bash
# Install build tools and dependencies
sudo apt update
sudo apt install build-essential git python3-dev libhdf5-dev cmake

# Verify versions
python3 --version  # Must be >= 3.7
cmake --version    # Must be >= 3.21
```

**Note**: If `cmake --version` shows < 3.21 (e.g., Ubuntu 20.04 has 3.16), see [CMake too old](#issue-cmake-not-found-or-version-too-old) in Troubleshooting.

#### Fedora/RedHat

```bash
sudo yum install gcc-c++ git python3-devel hdf5-devel cmake
```

#### Arch Linux

```bash
sudo pacman -S base-devel git python hdf5 cmake
```

#### macOS (Homebrew)

```bash
brew install hdf5 cmake python git
```

**Note**: Unlike Windows, HDF5 is **not bundled** on Linux/macOS. You must install it via your package manager (standard practice for C++ projects).

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/quentinducasse/mcnptoolspro.git
cd mcnptoolspro

# 2. Run the automated installation script
python3 install_dev.py
```

**What the script does:**
- ✓ Checks all prerequisites (Python, CMake, Git, GCC/Clang)
- ✓ Configures CMake for your platform
- ✓ Builds the C++ wrapper (`_mcnptools_wrap.so`)
- ✓ Copies the compiled wrapper to the Python package
- ✓ Installs the package in editable mode
- ✓ Verifies the installation works

That's it! The script handles everything automatically.

### Updating (Linux/macOS)

To update to the latest version:

```bash
cd mcnptoolspro
git pull origin main

# Re-run the installation script
python3 install_dev.py
```

**Note**: Python code changes are picked up automatically (editable mode), but C++ changes require rebuilding.

---

## 📋 System Requirements Summary

| Platform | Requirements |
|----------|-------------|
| **Windows** | Visual Studio 2017+ (MSVC), CMake 3.21+, Python 3.7+, Git<br/>**HDF5**: ✅ Bundled (no installation needed) |
| **Linux** | GCC 7+, CMake 3.21+, Python 3.7+, libhdf5-dev, build-essential, git<br/>**HDF5**: ⚙️ Install via package manager |
| **macOS** | Xcode Command Line Tools, CMake 3.21+, Python 3.7+, Git<br/>**HDF5**: ⚙️ Install via Homebrew |

**Python Dependencies**: None! mcnptoolspro is a pure C++ wrapper with no Python dependencies.

---

## 🐛 Troubleshooting

### Windows Issues

#### Issue: `Visual Studio not found`

**Solution**: Install Visual Studio 2017 or later

Download from: https://visualstudio.microsoft.com/downloads/

Choose "Desktop development with C++" workload.

#### Issue: `ImportError: DLL load failed`

**Note**: `hdf5.dll` is bundled, so this should rarely happen!

**Solutions**:

1. Verify `hdf5.dll` is present:
   ```powershell
   ls python\mcnptoolspro\hdf5.dll
   ```

2. Install Visual C++ Redistributable:
   - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Linux/macOS Issues

#### Issue: `CMake not found` or version too old

**Symptoms**:
- `CMake 3.21 or higher is required. You are running version 3.16.3`
- `cmake: command not found`
- `ModuleNotFoundError: No module named 'cmake'` when running cmake

**Solution**:

```bash
# 1. If you have cmake installed via pip, uninstall it (it's broken)
pip3 uninstall cmake -y

# 2. Install CMake 3.21+
# For Ubuntu 20.04 (easiest method):
sudo snap install cmake --classic
export PATH=/snap/bin:$PATH

# Verify
cmake --version  # Should show >= 3.21
which cmake      # Should show /snap/bin/cmake
```

**Alternative methods for CMake 3.21+**:
- **Ubuntu 22.04+**: `sudo apt install cmake` (already >= 3.21)
- **Kitware official repo** (Ubuntu 20.04):
  ```bash
  wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
  sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ focal main'
  sudo apt update && sudo apt install cmake
  ```

**IMPORTANT**: NEVER use `pip install cmake` - it creates a broken Python wrapper that conflicts with build tools.

#### Issue: `libhdf5 not found`

**Solution**: Install HDF5 development libraries

```bash
# Debian/Ubuntu
sudo apt-get install libhdf5-dev

# RedHat/CentOS
sudo yum install hdf5-devel

# Arch Linux
sudo pacman -S hdf5

# macOS
brew install hdf5
```

### All Platforms

#### Issue: VSCode shows yellow underline on `import mcnptoolspro`

**Cause**: VSCode/Pylance can't find the package or uses a different Python interpreter.

**Solution**:

1. **Select correct interpreter**:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type: `Python: Select Interpreter`
   - Choose the interpreter where mcnptoolspro is installed

2. **Reload VSCode**:
   - Press `Ctrl+Shift+P` → `Developer: Reload Window`

3. **Verify installation**:
   ```bash
   python -c "import mcnptoolspro; print('OK')"
   ```

**Note**: The yellow underline is just a linting warning. If the import works in terminal, it will work at runtime.

#### Issue: CMake configuration conflict

**Cause**: CMake cache from a previous build method.

**Solution**: Remove the cache file:

```bash
# Windows
Remove-Item build\CMakeCache.txt -ErrorAction SilentlyContinue

# Linux/macOS
rm -f build/CMakeCache.txt
```

Then retry the installation.

#### Issue: `ModuleNotFoundError: No module named 'mcnptoolspro'`

**Solution**: Installation failed or wrong Python environment

```bash
# Check installation
pip list | grep mcnptools

# If not listed, reinstall (see platform-specific instructions above)
cd mcnptoolspro/python
pip install -e .
```

---

## 🧪 Test Installation

### Quick Test

```python
import mcnptoolspro as m
print(f"mcnptoolspro loaded from: {m.__file__}")
```

### Full Test (if you have PTRAC files)

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

## 📊 Installation Methods Comparison

| Method | Platform | Use Case | Command |
|--------|----------|----------|---------|
| **Editable Install** | All | Recommended | `git clone ... && cd python && pip install -e .` |
| **Manual Build** | All | Expert control | `cmake ... && cmake --build ... && pip install -e .` |

---

## 🔄 Update mcnptoolspro

See platform-specific update instructions in [Windows Installation](#updating-windows) or [Linux/macOS Installation](#updating-linuxmacos).

---

## ✅ Installation Checklist

After installation, verify:

- [ ] `python -c "import mcnptoolspro"` works without errors
- [ ] Can create `Ptrac` object: `m.Ptrac('file.ptrac', m.Ptrac.ASC_PTRAC)`
- [ ] Can access other classes: `m.Mctal`, `m.Meshtal`
- [ ] Can read PTRAC files (if you have test files)

---

## 🆘 Still Having Issues?

1. **Check prerequisites**: Ensure CMake ≥ 3.13, Python ≥ 3.7
2. **Read platform-specific sections**: Windows or Linux/macOS
3. **Check troubleshooting**: See [Troubleshooting](#-troubleshooting) section
4. **Open an issue**: https://github.com/quentinducasse/mcnptoolspro/issues

When reporting issues, include:
- Operating system and version
- Python version (`python --version`)
- CMake version (`cmake --version`)
- Full error message
- Installation method attempted

---

**Happy PTRAC parsing!** 🚀

---

**Documentation**: [README.md](README.md) | [Technical Details](TECHNICAL_DETAILS.md)

**Support**: https://github.com/quentinducasse/mcnptoolspro/issues
