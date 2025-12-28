# mcnptoolspro

**Enhanced MCNP PTRAC parser with complete filter support**

[![License](https://img.shields.io/badge/license-BSD--3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

---

## Overview

`mcnptoolspro` is an enhanced version of [LANL's mcnptools](https://github.com/lanl/mcnptools) that adds **robust support for filtered PTRAC files** and **complete binary format support**.

### Built on LANL's Excellent Foundation

This project builds upon the outstanding work by Los Alamos National Laboratory (LANL) on the original [mcnptools](https://github.com/lanl/mcnptools) library. We are deeply grateful to Clell J. Solomon, Cameron Bates, Joel Kulesza, and the entire LANL team for creating and maintaining this essential tool for the MCNP community.

### What mcnptoolspro Adds

While the original mcnptools provides excellent basic PTRAC reading capabilities, it has incomplete support for:
1. **Filtered PTRAC files** - Files generated with MCNP filters (`tally=`, `filter=`, `event=`, `type=`), especially when combined
2. **Binary PTRAC files** - The binary format support had detection issues causing false positives

This enhanced version fixes these critical gaps while maintaining 100% API compatibility.

### Key Improvements

- ✅ **Complete filter support**: `tally`, `filter`, `event`, `type`, and all combinations
- ✅ **All formats supported**: ASCII, Binary, and HDF5 PTRAC files
- ✅ **Bug fixes**: Resolves infinite loops and parsing errors with filtered PTRAC files
- ✅ **Drop-in replacement**: Same API as mcnptools, just import `mcnptoolspro` instead
- ✅ **Production-ready**: Validated with 18 test files covering all formats and filters
- ✅ **High performance**: Average load time < 0.1s, even for large files

---

## Installation

### Recommended Method

```bash
# 1. Clone the repository
git clone https://github.com/quentinducasse/mcnptoolspro.git
cd mcnptoolspro

# 2. Install in editable mode
cd python
pip install -e .
```

**For detailed installation instructions, troubleshooting, and alternative methods, see [INSTALL.md](INSTALL.md).**

### Requirements

- Python 3.7+
- CMake 3.13+
- C++ compiler (Visual Studio on Windows, GCC/Clang on Linux/macOS)
- Git
- HDF5 (bundled on Windows, install via package manager on Linux/macOS)

---

## Usage

```python
import mcnptoolspro as m

# Read ASCII PTRAC file
ptrac = m.Ptrac('output.ptrac', m.Ptrac.ASC_PTRAC)

# Read Binary PTRAC file
ptrac = m.Ptrac('output.ptrac', m.Ptrac.BIN_PTRAC)

# Read HDF5 PTRAC file
ptrac = m.Ptrac('output.h5', m.Ptrac.HDF5_PTRAC)

# Read first 10 histories
histories = ptrac.ReadHistories(10)

# Process events
for i, hist in enumerate(histories):
    num_events = hist.GetNumEvents()
    print(f"History {i+1}: {num_events} events")

    # Access first event
    event = hist.GetEvent(0)
    if event.Has(26):  # Energy field
        energy = event.Get(26)
        print(f"  First event energy: {energy:.6f} MeV")
```

**The API is identical to mcnptools** - just replace `import mcnptools` with `import mcnptoolspro`.

### Supported Formats

- ✅ **ASCII** (`ASC_PTRAC`) - Text format, human-readable
- ✅ **Binary** (`BIN_PTRAC`) - Binary format, more compact
- ✅ **HDF5** (`HDF5_PTRAC`) - HDF5 format, requires HDF5 library

---

## Supported PTRAC Filters

mcnptoolspro correctly parses PTRAC files generated with the following MCNP filters:

| Filter | MCNP Command | Description |
|--------|--------------|-------------|
| **tally** | `tally=4` | Only particles contributing to specified tally |
| **filter** | `filter=0.0,10.0,X 0,1,U 1.0,2,ERG` | Only particles events in which the particle’s x-coordinate is between 0 and 10 cm and the particle’s x-axis cosine is between 0 and 1 and the particle’s energy is between 1 and 2MeV |
| **event** | `event=src,bnk,ter` | Only specified event types |
| **type** | `type=h,t` | Only specified particle types |
| **Combined** | Multiple filters | Any combination of the above |

### Example MCNP Input

```
ptrac file=asc max=-1000 tally=4 filter=-200,200,X event=src,bnk,ter type=n,h,t write=all
```

This complex filter combination (tally + filter + event + type) is fully supported by mcnptoolspro.

---

## What's Fixed

### Critical Bugs Resolved

1. **Infinite loop with combined filters**
   - Original mcnptools enters infinite loop when reading PTRAC files with `nkw=3` (combined filters)
   - **Fixed** with simplified deterministic header parsing

2. **Tally filter detection failure**
   - Original mcnptools fails to detect tally filters, causing parsing errors
   - **Fixed** by correctly checking for negative keyword values

3. **Incorrect skip logic**
   - Original mcnptools skips wrong number of header lines for filtered files
   - **Fixed** with unified skip logic based on filter type

### Technical Details

For in-depth technical explanations of the C++ code modifications, see **[TECHNICAL_DETAILS.md](doc/TECHNICAL_DETAILS.md)**.

---

## Testing Status

### Comprehensive Validation (18 Test Files)

mcnptoolspro has been extensively tested with 18 PTRAC files in [tests/test_data_github](tests/test_data_github):

- ✅ **ASCII**: 13/13 files (100%) - All filter combinations for MCNP 6.2 and 6.3
- ✅ **Binary**: 4/4 files (100%) - Including production simulations
- ✅ **HDF5**: 1/1 file (100%) - Modern HDF5 format support

### MCNP Version Compatibility

- ✅ **MCNP 6.2**: Fully supported
- ✅ **MCNP 6.3**: Fully supported with special tally handling

### Performance Metrics

All 18 test files load in **< 0.2 seconds** (average: 0.07s), including:
- Large files (up to 20 MB)
- Complex filter combinations (tally + event + type + filter)
- Binary format (as fast as ASCII)

**Run comprehensive tests**: `python examples/test_all_ptrac_files.py`

---

## Examples

### Interactive Demos (Perfect for First-Time Users!)

Run interactive demonstrations to see concrete results:

```bash
cd mcnptoolspro/examples
python run_all_demos.py
```

This runs all 6 filter demos showing:
- ✅ Real event counts from sample PTRAC files
- ✅ Filter effects visualized (file size reduction)
- ✅ Comparison between filter types
- ✅ Concrete proof that mcnptoolspro works!

**Individual demos**:
```bash
python demo_filter_none.py    # Baseline (no filter)
python demo_filter_event.py   # Event filter (src, bnk, ter)
python demo_filter_type.py    # Type filter (n, h, t)
python demo_filter_filter.py  # Filter card (position/angle/energy)
python demo_filter_tally.py   # Tally filter (tally=4)
python demo_filter_all.py     # Combined filters (max reduction)
```

**Example output** (demo_filter_all.py):
```
FILTER COMPARISON:
  Baseline (no filter):  63 events (100%)
  COMBINED (all):         2 events (  3%)

FILE SIZE REDUCTION:
  Combined filters reduce file size by ~97%!

KEY INSIGHT:
  This is what mcnptoolspro fixes - the original mcnptools
  would FAIL or enter infinite loop with combined filters!
```

See [examples/README.md](examples/README.md) for details.

---

## Testing

### Unit Tests

```bash
cd mcnptoolspro/tests
python test_basic.py
```

Expected output:
```
[OK] Import mcnptoolspro
[OK] Ptrac constants accessible
[OK] Ptrac object creation
[OK] Read histories (2 histories, 35 events in first)
[OK] Event access (35 events accessible)

All tests passed (5/5)
```

### Integration Tests

```bash
python test_all_filters.py
```

Expected output:
```
Testing filter: none     ... OK (63 events)
Testing filter: event    ... OK (9 events)
Testing filter: type     ... OK (13 events)
Testing filter: filter   ... OK (15 events)
Testing filter: tally    ... OK (319 events)
Testing filter: all      ... OK (2 events)

All tests passed (6/6 filters)
```

---

## Documentation

- [INSTALL.md](INSTALL.md) - Installation guide for all platforms
- [CHANGELOG.md](doc/CHANGELOG.md) - Version history and changes
- [TECHNICAL_DETAILS.md](doc/TECHNICAL_DETAILS.md) - C++ code modifications explained
- [tests/README.md](tests/README.md) - Test suite documentation
- [examples/README.md](examples/README.md) - Interactive demos and usage examples

---

## License

This project is licensed under the **BSD-3-Clause License**, same as the original mcnptools.

### Credits

**Original mcnptools** by:
- Clell J. (CJ) Solomon
- Cameron Bates
- Joel Kulesza
- Los Alamos National Laboratory

**Filter support enhancements** by:
- Quentin Ducasse (2024-2025)
- Developed for the DECIMA project

---

## Citation

If you use mcnptoolspro, please cite both:

**Original mcnptools**:
> C. R. Bates et al., "The MCNPTools Package: Installation and Use",
> Los Alamos National Laboratory Tech. Report LA-UR-22-28935, 2022.
> [doi:10.2172/1884737](http://dx.doi.org/10.2172/1884737)

**mcnptoolspro enhancements**:
> Q. Ducasse, "mcnptoolspro: Enhanced MCNP PTRAC parser with complete filter support",
> GitHub repository, 2025. https://github.com/quentinducasse/mcnptoolspro

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## Contact

**Quentin Ducasse**
- GitHub: [@quentinducasse](https://github.com/quentinducasse)
- Email: quentin.ducasse@gmail.com

**Issues**: https://github.com/quentinducasse/mcnptoolspro/issues

---

## Related Projects

- [LANL mcnptools](https://github.com/lanl/mcnptools) - Original library
- [DECIMA](https://github.com/quentinducasse/DECIMA) - Monte Carlo simulation analysis platform
- [MCNP](https://mcnp.lanl.gov/) - Monte Carlo N-Particle transport code
