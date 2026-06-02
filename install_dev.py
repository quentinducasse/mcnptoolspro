#!/usr/bin/env python3
"""
Development installer for mcnptoolspro.

On Windows this script installs HDF5 with a local vcpkg checkout when the HDF5
development files are missing.

Important: this script does not use CMAKE_TOOLCHAIN_FILE for vcpkg. The
shacl-F5_CXX dependency wraps find_package(), and the vcpkg HDF5 wrapper can
recurse through that path. Instead, we pass HDF5/ZLIB locations directly.
"""

from __future__ import annotations

import multiprocessing
import os
import platform
import shutil
import site
import subprocess
import sys
from pathlib import Path


BUILD_DIR_NAME = "build"
WINDOWS_GENERATOR = "Visual Studio 17 2022"
WINDOWS_TRIPLET = "x64-windows"
RUNTIME_DLLS = ("hdf5.dll", "z.dll", "aec.dll", "szip.dll")


def print_header(message: str) -> None:
    print()
    print("=" * 76)
    print(message.center(76))
    print("=" * 76)
    print()


def print_step(step_num: int, total: int, message: str) -> None:
    print(f"[{step_num}/{total}] {message}...")
    print()


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    print(f"  Running: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(f"  ERROR: command failed with exit code {exc.returncode}")
        if exc.stdout:
            print()
            print("  Output:")
            for line in exc.stdout.splitlines():
                print(f"  {line}")
        print()
        return False

    if result.stdout:
        for line in result.stdout.splitlines():
            print(f"  {line}")
        print()

    return True


def command_output(cmd: list[str]) -> str | None:
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def find_vcpkg_root(root_dir: Path) -> Path | None:
    candidates = []

    env_root = os.environ.get("VCPKG_ROOT")
    if env_root:
        candidates.append(Path(env_root))

    candidates.extend(
        [
            root_dir.parent / "vcpkg",
            Path.home() / "SOFTWARES" / "vcpkg",
            Path("C:/vcpkg"),
        ]
    )

    for candidate in candidates:
        if (candidate / "vcpkg.exe").exists():
            return candidate.resolve()

    return None


def windows_hdf5_paths(root_dir: Path) -> dict[str, Path] | None:
    vcpkg_root = find_vcpkg_root(root_dir)
    if not vcpkg_root:
        return None

    prefix = vcpkg_root / "installed" / WINDOWS_TRIPLET
    return {
        "vcpkg_root": vcpkg_root,
        "prefix": prefix,
        "hdf5_dir": prefix / "share" / "hdf5",
        "include": prefix / "include" / "hdf5.h",
        "hdf5_lib": prefix / "lib" / "hdf5.lib",
        "zlib_lib": prefix / "lib" / "z.lib",
        "bin": prefix / "bin",
    }


def windows_hdf5_is_ready(root_dir: Path) -> bool:
    hdf5 = windows_hdf5_paths(root_dir)
    if hdf5 is None:
        return False

    required = [
        hdf5["include"],
        hdf5["hdf5_lib"],
        hdf5["zlib_lib"],
        *(hdf5["bin"] / dll for dll in RUNTIME_DLLS),
    ]
    return all(path.exists() for path in required)


def ensure_windows_hdf5(root_dir: Path) -> bool:
    if platform.system() != "Windows" or windows_hdf5_is_ready(root_dir):
        return True

    print("  HDF5 development files were not found.")
    print("  Installing HDF5 with local vcpkg...")
    print()

    vcpkg_root = find_vcpkg_root(root_dir)
    if vcpkg_root is None:
        vcpkg_root = (root_dir.parent / "vcpkg").resolve()
        if not run_command(
            [
                "git",
                "clone",
                "https://github.com/microsoft/vcpkg.git",
                str(vcpkg_root),
            ]
        ):
            return False

    vcpkg_exe = vcpkg_root / "vcpkg.exe"
    if not vcpkg_exe.exists():
        bootstrap = vcpkg_root / "bootstrap-vcpkg.bat"
        if not bootstrap.exists():
            print(f"  ERROR: vcpkg bootstrap script not found: {bootstrap}")
            print()
            return False
        if not run_command([str(bootstrap)], cwd=vcpkg_root):
            return False

    if not run_command(
        [
            str(vcpkg_exe),
            "install",
            f"hdf5:{WINDOWS_TRIPLET}",
            "--disable-metrics",
        ],
        cwd=vcpkg_root,
    ):
        return False

    if not windows_hdf5_is_ready(root_dir):
        print("  ERROR: HDF5 installation finished, but required files are still missing.")
        print()
        return False

    print("  [OK] HDF5 installed with vcpkg")
    print()
    return True


def check_prerequisites(root_dir: Path) -> bool:
    print_step(1, 5, "Checking prerequisites")
    issues: list[str] = []

    if sys.version_info < (3, 7):
        issues.append(
            f"Python 3.7+ required, found {sys.version_info.major}.{sys.version_info.minor}"
        )
    else:
        print(
            f"  [OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

    cmake_version = command_output(["cmake", "--version"])
    if cmake_version:
        print(f"  [OK] {cmake_version.splitlines()[0]}")
    else:
        issues.append("CMake not found")

    git_version = command_output(["git", "--version"])
    if git_version:
        print(f"  [OK] {git_version}")
    else:
        issues.append("Git not found")

    system = platform.system()
    print(f"  [OK] Platform: {system}")

    if system == "Windows":
        vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
        if vswhere.exists():
            print("  [OK] Visual Studio detected")
        else:
            issues.append('Visual Studio with "Desktop development with C++" not found')

        if not issues and not ensure_windows_hdf5(root_dir):
            issues.append("Could not install HDF5 with vcpkg")

        hdf5 = windows_hdf5_paths(root_dir)
        if not hdf5:
            issues.append(
                "vcpkg not found. Set VCPKG_ROOT or install it next to this repository."
            )
        else:
            print(f"  [OK] vcpkg: {hdf5['vcpkg_root']}")
            for label in ("include", "hdf5_lib", "zlib_lib"):
                if hdf5[label].exists():
                    print(f"  [OK] {hdf5[label]}")
                else:
                    issues.append(f"Missing {hdf5[label]}")

            for dll in RUNTIME_DLLS:
                dll_path = hdf5["bin"] / dll
                if not dll_path.exists():
                    issues.append(f"Missing runtime DLL: {dll_path}")

            if hdf5 and not issues:
                print("  [OK] HDF5/ZLIB runtime DLLs found")

    print()

    if issues:
        print("  Prerequisites missing:")
        for issue in issues:
            print(f"    [X] {issue}")
        if system == "Windows":
            print()
            print("  Install HDF5 with:")
            print(r"    C:\Users\ducasse-que\SOFTWARES\vcpkg\vcpkg.exe install hdf5:x64-windows")
        print()
        return False

    return True


def clean_cmake_cache(build_dir: Path) -> None:
    if not build_dir.exists():
        return

    stale_files = [
        build_dir / "CMakeCache.txt",
        build_dir / "cmake_install.cmake",
    ]

    for stale_file in stale_files:
        if stale_file.exists():
            stale_file.unlink()
            print(f"  [OK] Removed stale file: {stale_file}")

    cmake_files = build_dir / "CMakeFiles"
    if cmake_files.exists():
        shutil.rmtree(cmake_files)
        print(f"  [OK] Removed stale directory: {cmake_files}")

    if stale_files or cmake_files.exists():
        print()


def cmake_configure_args(root_dir: Path, build_dir: Path) -> list[str]:
    cmd = [
        "cmake",
        "-S",
        str(root_dir),
        "-B",
        str(build_dir),
        "-DCMAKE_BUILD_TYPE=Release",
        "-DBUILD_TESTING=OFF",
    ]

    if platform.system() == "Windows":
        hdf5 = windows_hdf5_paths(root_dir)
        if hdf5 is None:
            raise RuntimeError("vcpkg/HDF5 paths are unavailable")

        cmd.extend(
            [
                f"-DCMAKE_PREFIX_PATH={hdf5['prefix']}",
                f"-DHDF5_DIR={hdf5['hdf5_dir']}",
                f"-DZLIB_ROOT={hdf5['prefix']}",
                "-G",
                WINDOWS_GENERATOR,
            ]
        )

    return cmd


def configure_cmake(root_dir: Path) -> bool:
    print_step(2, 5, "Configuring CMake build")
    build_dir = root_dir / BUILD_DIR_NAME

    clean_cmake_cache(build_dir)
    return run_command(cmake_configure_args(root_dir, build_dir))


def build_wrapper(root_dir: Path) -> bool:
    print_step(3, 5, "Building C++ wrapper")
    build_dir = root_dir / BUILD_DIR_NAME
    jobs = "8" if platform.system() == "Windows" else str(multiprocessing.cpu_count())

    cmd = [
        "cmake",
        "--build",
        str(build_dir),
        "--target",
        "_mcnptools_wrap",
    ]

    if platform.system() == "Windows":
        cmd.extend(["--config", "Release"])

    cmd.extend(["-j", jobs])
    return run_command(cmd)


def copy_built_artifacts(root_dir: Path) -> bool:
    print_step(4, 5, "Copying Python extension and runtime libraries")

    build_dir = root_dir / BUILD_DIR_NAME
    package_dir = root_dir / "python" / "mcnptoolspro"
    package_dir.mkdir(parents=True, exist_ok=True)

    if platform.system() == "Windows":
        wrapper_src = build_dir / "python" / "mcnptoolspro" / "Release" / "_mcnptools_wrap.pyd"
        wrapper_dst = package_dir / "_mcnptools_wrap.pyd"
    else:
        wrapper_src = build_dir / "python" / "mcnptoolspro" / "_mcnptools_wrap.so"
        wrapper_dst = package_dir / "_mcnptools_wrap.so"

    if not wrapper_src.exists():
        print(f"  ERROR: compiled wrapper not found at {wrapper_src}")
        print()
        return False

    shutil.copy2(wrapper_src, wrapper_dst)
    print(f"  [OK] Copied: {wrapper_dst}")

    if platform.system() == "Windows":
        hdf5 = windows_hdf5_paths(root_dir)
        if hdf5 is None:
            print("  ERROR: vcpkg/HDF5 paths are unavailable")
            print()
            return False

        for dll in RUNTIME_DLLS:
            src = hdf5["bin"] / dll
            dst = package_dir / dll
            shutil.copy2(src, dst)
            print(f"  [OK] Copied: {dst}")

    print()
    return True


def install_package(root_dir: Path) -> bool:
    print_step(5, 5, "Installing Python package in editable mode")

    python_dir = root_dir / "python"
    user_site = Path(site.getusersitepackages())
    user_site.mkdir(parents=True, exist_ok=True)

    pth_file = user_site / "mcnptoolspro.pth"
    pth_file.write_text(str(python_dir) + "\n", encoding="utf-8")

    print(f"  [OK] Created: {pth_file}")
    print(f"  [OK] Points to: {python_dir}")
    print()

    return True


def verify_installation(root_dir: Path) -> bool:
    print_header("Verifying installation")

    test_hdf5 = root_dir / "tests" / "test_data_github" / "example_ptrac_3_HDF5.h5"
    verification_code = f"""
import sys
import mcnptoolspro as m

print("  [OK] mcnptoolspro imported successfully")
print(f"  [OK] Location: {{m.__file__}}")
print(f"  [OK] Ptrac.ASC_PTRAC = {{m.Ptrac.ASC_PTRAC}}")
print(f"  [OK] Ptrac.BIN_PTRAC = {{m.Ptrac.BIN_PTRAC}}")
print(f"  [OK] Ptrac.HDF5_PTRAC = {{m.Ptrac.HDF5_PTRAC}}")

test_hdf5 = r"{test_hdf5}"
if test_hdf5:
    p = m.Ptrac(test_hdf5, m.Ptrac.HDF5_PTRAC)
    histories = p.ReadHistories(1)
    print(f"  [OK] HDF5 test histories read: {{len(histories)}}")
"""

    try:
        result = subprocess.run(
            [sys.executable, "-c", verification_code],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        print(f"  [X] Verification error: {exc}")
        print()
        return False

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print_header("Installation verification failed")
        return False

    print_header("Installation successful")
    print("You can now use mcnptoolspro in your Python scripts.")
    print()
    return True


def main() -> int:
    print_header("mcnptoolspro - Development Installation")

    print("This script will:")
    print("  1. Check prerequisites")
    print("  2. Configure CMake with explicit HDF5/ZLIB paths")
    print("  3. Build the C++ wrapper")
    print("  4. Copy the Python extension and runtime DLLs")
    print("  5. Install the Python package in editable mode")
    print()

    root_dir = Path(__file__).parent.resolve()
    print(f"Working directory: {root_dir}")
    print(f"Build directory:   {root_dir / BUILD_DIR_NAME}")
    print()

    steps = (
        lambda: check_prerequisites(root_dir),
        lambda: configure_cmake(root_dir),
        lambda: build_wrapper(root_dir),
        lambda: copy_built_artifacts(root_dir),
        lambda: install_package(root_dir),
    )

    for step in steps:
        if not step():
            return 1

    return 0 if verify_installation(root_dir) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print()
        print("Installation interrupted by user.")
        raise SystemExit(1)
