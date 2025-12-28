#!/usr/bin/env python3
"""
Development Installation Script for mcnptoolspro

Automatically builds the C++ wrapper and installs the package in editable mode.
Works on Windows, Linux, and macOS.

Usage:
    python install_dev.py
"""

import sys
import os
import platform
import subprocess
import shutil
from pathlib import Path


def print_header(message):
    """Print a formatted header"""
    print()
    print("=" * 76)
    print(message.center(76))
    print("=" * 76)
    print()


def print_step(step_num, message):
    """Print a step message"""
    print(f"[{step_num}/4] {message}...")
    print()


def run_command(cmd, cwd=None, shell=False):
    """Run a command and print output in real-time"""
    print(f"  Running: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    print()

    try:
        # Use shell=True on Windows for commands like 'copy'
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Print output
        if result.stdout:
            for line in result.stdout.splitlines():
                print(f"  {line}")
            print()

        return True

    except subprocess.CalledProcessError as e:
        print(f"  ERROR: Command failed with exit code {e.returncode}")
        if e.stdout:
            print()
            print("  Output:")
            for line in e.stdout.splitlines():
                print(f"  {line}")
        print()
        return False


def check_prerequisites():
    """Check if required tools are installed"""
    print_step(1, "Checking prerequisites")

    issues = []

    # Check Python version
    py_version = sys.version_info
    if py_version < (3, 7):
        issues.append(f"Python 3.7+ required (found {py_version.major}.{py_version.minor})")
    else:
        print(f"  [OK] Python {py_version.major}.{py_version.minor}.{py_version.micro}")

    # Check CMake
    try:
        result = subprocess.run(['cmake', '--version'], capture_output=True, text=True)
        cmake_version = result.stdout.split('\n')[0]
        print(f"  [OK] {cmake_version}")
    except FileNotFoundError:
        issues.append("CMake not found - install from https://cmake.org/download/")

    # Check Git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        git_version = result.stdout.strip()
        print(f"  [OK] {git_version}")
    except FileNotFoundError:
        issues.append("Git not found - install from https://git-scm.com/")

    # Platform-specific checks
    system = platform.system()
    print(f"  [OK] Platform: {system}")

    if system == 'Windows':
        # Check for Visual Studio
        vswhere_path = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
        if os.path.exists(vswhere_path):
            print("  [OK] Visual Studio detected")
        else:
            issues.append("Visual Studio not found - install from https://visualstudio.microsoft.com/")

    print()

    if issues:
        print("  Prerequisites missing:")
        for issue in issues:
            print(f"    [X] {issue}")
        print()
        return False

    return True


def configure_cmake(root_dir):
    """Configure CMake build"""
    print_step(2, "Configuring CMake build")

    build_dir = root_dir / 'build'
    system = platform.system()

    # Build CMake command
    cmd = [
        'cmake',
        '-S', str(root_dir),
        '-B', str(build_dir),
        '-DCMAKE_BUILD_TYPE=Release',
        '-DBUILD_TESTING=OFF'
    ]

    # Add Visual Studio generator on Windows
    if system == 'Windows':
        cmd.extend(['-G', 'Visual Studio 17 2022'])

    return run_command(cmd)


def build_wrapper(root_dir):
    """Build the C++ wrapper"""
    print_step(3, "Building C++ wrapper")

    build_dir = root_dir / 'build'
    system = platform.system()

    # Build command
    cmd = [
        'cmake',
        '--build', str(build_dir),
        '--target', '_mcnptools_wrap'
    ]

    # Add config for Windows
    if system == 'Windows':
        cmd.extend(['--config', 'Release'])

    # Add parallel build flag
    if system != 'Windows':
        import multiprocessing
        cmd.extend(['-j', str(multiprocessing.cpu_count())])
    else:
        cmd.extend(['-j', '8'])

    if not run_command(cmd):
        return False

    # Copy the compiled wrapper to the Python package directory
    print("  Copying compiled wrapper to Python package...")
    print()

    python_pkg_dir = root_dir / 'python' / 'mcnptoolspro'

    if system == 'Windows':
        wrapper_src = build_dir / 'python' / 'mcnptoolspro' / 'Release' / '_mcnptools_wrap.pyd'
        wrapper_dst = python_pkg_dir / '_mcnptools_wrap.pyd'
    else:
        wrapper_src = build_dir / 'python' / 'mcnptoolspro' / '_mcnptools_wrap.so'
        wrapper_dst = python_pkg_dir / '_mcnptools_wrap.so'

    if not wrapper_src.exists():
        print(f"  ERROR: Compiled wrapper not found at: {wrapper_src}")
        print()
        return False

    try:
        shutil.copy2(wrapper_src, wrapper_dst)
        print(f"  [OK] Copied: {wrapper_dst.name}")
        print()
        return True
    except Exception as e:
        print(f"  ERROR: Failed to copy wrapper: {e}")
        print()
        return False


def install_package(root_dir):
    """Install the Python package in editable mode"""
    print_step(4, "Installing Python package in editable mode")

    python_dir = root_dir / 'python'

    # First, ensure pip itself is up to date
    print("  Ensuring pip is up to date...")
    print()
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                   capture_output=True)

    # Install in editable mode
    cmd = [sys.executable, '-m', 'pip', 'install', '--no-build-isolation', '-e', '.']

    return run_command(cmd, cwd=str(python_dir))


def verify_installation():
    """Verify that the installation works"""
    print()
    print("=" * 76)
    print("Verifying installation...".center(76))
    print("=" * 76)
    print()

    # Force reimport by clearing any cached imports
    if 'mcnptoolspro' in sys.modules:
        del sys.modules['mcnptoolspro']
    if '_mcnptools_wrap' in sys.modules:
        del sys.modules['_mcnptools_wrap']

    try:
        import mcnptoolspro as m
        print(f"  [OK] mcnptoolspro imported successfully")
        print(f"  [OK] Location: {m.__file__}")
        print()

        # Check that Ptrac class is accessible
        if hasattr(m.Ptrac, 'ASC_PTRAC'):
            print("  [OK] Ptrac.ASC_PTRAC constant accessible")
        if hasattr(m.Ptrac, 'BIN_PTRAC'):
            print("  [OK] Ptrac.BIN_PTRAC constant accessible")
        if hasattr(m.Ptrac, 'HDF5_PTRAC'):
            print("  [OK] Ptrac.HDF5_PTRAC constant accessible")

        print()
        print("=" * 76)
        print("Installation successful!".center(76))
        print("=" * 76)
        print()
        print("You can now use mcnptoolspro in your Python scripts.")
        print()

        return True

    except ImportError as e:
        print(f"  [X] Import failed: {e}")
        print()
        print("=" * 76)
        print("Installation verification failed".center(76))
        print("=" * 76)
        print()
        return False


def main():
    """Main installation routine"""
    print_header("mcnptoolspro - Development Installation")

    print("This script will:")
    print("  1. Check prerequisites")
    print("  2. Configure CMake build")
    print("  3. Build C++ wrapper")
    print("  4. Install Python package in editable mode")
    print()

    # Get root directory (where this script is located)
    root_dir = Path(__file__).parent.resolve()
    print(f"Working directory: {root_dir}")
    print()

    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("Please install missing prerequisites and try again.")
        return 1

    # Step 2: Configure CMake
    if not configure_cmake(root_dir):
        print("CMake configuration failed. Check the error messages above.")
        return 1

    # Step 3: Build wrapper
    if not build_wrapper(root_dir):
        print("Build failed. Check the error messages above.")
        return 1

    # Step 4: Install package
    if not install_package(root_dir):
        print("Package installation failed. Check the error messages above.")
        return 1

    # Verify installation
    if not verify_installation():
        return 1

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print()
        print("Installation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
