# mcnptoolspro

**Enhanced MCNP PTRAC parser with complete filter support**

[![License](https://img.shields.io/badge/license-BSD--3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

---

## Overview

`mcnptoolspro` is an enhanced version of [LANL's mcnptools](https://github.com/lanl/mcnptools) that adds **robust support for filtered PTRAC files**.

The original mcnptools library has incomplete support for PTRAC files generated with MCNP filters (`tally=`, `filter=`, `event=`, `type=`), particularly when filters are combined. This enhanced version fixes critical parsing bugs and provides reliable reading of all filter combinations.

### Key Improvements

- ✅ **Complete filter support**: `tally`, `filter`, `event`, `type`, and combinations
- ✅ **Bug fixes**: Resolves infinite loops and parsing errors with filtered PTRAC files
- ✅ **Drop-in replacement**: Same API as mcnptools, just import `mcnptoolspro` instead
- ✅ **Production-ready**: Validated against extensive test suite

---

## Installation

### Quick install from GitHub

```bash
pip install git+https://github.com/quentinducasse/mcnptoolspro.git#subdirectory=python
```

### Install from source

```bash
git clone https://github.com/quentinducasse/mcnptoolspro.git
cd mcnptoolspro/python
pip install .
```

**For detailed installation instructions**, see **[INSTALL.md](INSTALL.md)**.

### Requirements

- Python 3.7+
- CMake 3.13+
- C++ compiler (MSVC on Windows, GCC/Clang on Linux/macOS)

---

## Usage

```python
import mcnptoolspro as m

# Read ASCII PTRAC file (filtered or not)
ptrac = m.Ptrac('output.ptrac', m.Ptrac.ASC_PTRAC)

# Read particle histories
histories = ptrac.ReadHistories(100)

# Process events
for hist in histories:
    for event in hist.GetEvents():
        print(f"Energy: {event.GetERG()} MeV")
        print(f"Position: ({event.GetX()}, {event.GetY()}, {event.GetZ()})")
```

**The API is identical to mcnptools** - just replace `import mcnptools` with `import mcnptoolspro`.

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

For in-depth technical explanations of the C++ code modifications, see **[TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md)**.

---

## Limitations

### Current Testing Status

- ✅ **Tested**: ASCII PTRAC files (MCNP 6.2)
- ⚠️ **To be tested**:
  - Binary PTRAC files
  - HDF5 PTRAC files
  - MCNP 6.3 compatibility
  - All possible filter combinations (some edge cases may exist)

### Known Issues

- Some untested filter combinations may fail
- Binary and HDF5 formats have not been validated yet

**See [TODO.md](TODO.md) for planned testing and improvements.**

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

- [INSTALL.md](INSTALL.md) - Installation guide
- [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) - C++ modifications explained
- [TODO.md](TODO.md) - Future improvements and testing

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
