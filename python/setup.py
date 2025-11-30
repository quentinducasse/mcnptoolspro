"""
mcnptoolspro - Enhanced MCNP PTRAC parser with full filter support

This setup.py provides standalone pip installation capability.
It builds the C++ extension using CMake and installs the Python package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


class CMakeBuild(build_ext):
    """Custom build extension that uses CMake to compile C++ code"""

    def run(self):
        # Check CMake is installed
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build mcnptoolspro. "
                "Install it with: pip install cmake"
            )

        # Build each extension
        for ext in self.extensions:
            self.build_cmake(ext)

        # Don't call super().run() because CMake already built the extension
        # Calling super().run() would try to compile sources=[] which fails

    def build_cmake(self, ext):
        """Run CMake build process"""

        # Get paths
        source_dir = Path(__file__).parent.parent.absolute()
        build_dir = source_dir / 'build'
        python_dir = source_dir / 'python'
        package_dir = python_dir / 'mcnptoolspro'

        # Create build directory
        build_dir.mkdir(exist_ok=True)

        # CMake configure
        print(f"Configuring CMake in {build_dir}")
        cmake_args = [
            'cmake',
            '-S', str(source_dir),
            '-B', str(build_dir),
            '-DCMAKE_BUILD_TYPE=Release',
            '-DBUILD_TESTING=OFF',  # Skip tests to avoid gtest errors
        ]

        # Add platform-specific args
        if sys.platform.startswith('win'):
            cmake_args.extend([
                '-G', 'Visual Studio 17 2022',
                '-A', 'x64',
            ])

        subprocess.check_call(cmake_args)

        # CMake build
        print("Building with CMake...")
        build_args = [
            'cmake',
            '--build', str(build_dir),
            '--config', 'Release',
            '--target', '_mcnptools_wrap',
            '-j', str(os.cpu_count() or 4)
        ]

        subprocess.check_call(build_args)

        # Copy compiled wrapper to both source and build directories
        print("Copying compiled wrapper to package...")

        if sys.platform.startswith('win'):
            # Windows: .pyd file
            wrapper_src = build_dir / 'python' / 'mcnptoolspro' / 'Release' / '_mcnptools_wrap.pyd'
            wrapper_name = '_mcnptools_wrap.pyd'
        else:
            # Linux/Mac: .so file
            wrapper_src = build_dir / 'python' / 'mcnptoolspro' / '_mcnptools_wrap.so'
            wrapper_name = '_mcnptools_wrap.so'

        if not wrapper_src.exists():
            raise RuntimeError(
                f"Compiled wrapper not found at {wrapper_src}\n"
                f"Build may have failed. Check CMake output above."
            )

        # Copy to source directory (for development)
        wrapper_dst_source = package_dir / wrapper_name
        shutil.copy(str(wrapper_src), str(wrapper_dst_source))
        print(f"[OK] Copied {wrapper_src} -> {wrapper_dst_source}")

        # Copy to build directory (for installation)
        ext_path = Path(self.get_ext_fullpath(ext.name))
        ext_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(wrapper_src), str(ext_path))
        print(f"[OK] Copied {wrapper_src} -> {ext_path}")


# Read version from CMakeLists.txt
def get_version():
    """Extract version from CMakeLists.txt"""
    cmake_file = Path(__file__).parent.parent / 'CMakeLists.txt'

    with open(cmake_file, 'r') as f:
        for line in f:
            if 'project(' in line and 'VERSION' in line:
                # Extract version number
                import re
                match = re.search(r'VERSION\s+(\d+\.\d+\.\d+)', line)
                if match:
                    return match.group(1)

    return '1.0.0'  # Fallback version


# Read long description from README
def get_long_description():
    """Get long description from README"""
    readme_path = Path(__file__).parent.parent / 'README_MCNPTOOLSPRO.md'

    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "Enhanced MCNP PTRAC parser with full filter support"


setup(
    name='mcnptoolspro',
    version=get_version(),

    author='Quentin Ducasse (based on LANL mcnptools)',
    author_email='quentin.ducasse@gmail.com',

    description='Enhanced MCNP PTRAC parser with full filter support (6/6 filters)',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    url='https://github.com/quentinducasse/mcnptoolspro',
    project_urls={
        'Bug Tracker': 'https://github.com/quentinducasse/mcnptoolspro/issues',
        'Documentation': 'https://github.com/quentinducasse/mcnptoolspro#readme',
        'Source Code': 'https://github.com/quentinducasse/mcnptoolspro',
    },

    # Packages
    packages=['mcnptoolspro'],
    package_dir={'mcnptoolspro': 'mcnptoolspro'},
    include_package_data=True,

    # Include compiled extension and all .py files
    package_data={
        'mcnptoolspro': [
            '*.pyd',  # Windows compiled extension
            '*.so',   # Linux/Mac compiled extension
            '*.dll',  # Windows DLL dependencies (hdf5.dll)
            '*.py',
        ]
    },

    # Extension (built by CMake)
    ext_modules=[Extension('mcnptoolspro._mcnptools_wrap', sources=[])],
    cmdclass={'build_ext': CMakeBuild},

    # Requirements
    python_requires='>=3.7',
    install_requires=[
        # No Python dependencies - pure C++ wrapper
    ],

    # Extras for development
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov',
            'black',
            'flake8',
        ],
        'build': [
            'cmake>=3.13',
            'build',
            'twine',
        ]
    },

    # Metadata
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
    ],

    keywords='mcnp ptrac particle-transport nuclear-physics monte-carlo',

    # Not zip-safe because of compiled extension
    zip_safe=False,
)
