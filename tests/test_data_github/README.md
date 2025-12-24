# PTRAC Test Files for GitHub

This directory contains a curated selection of PTRAC files for testing and demonstration purposes.

## Files Overview

**Total: 18 files (100% working)**
- 13 ASCII files
- 4 Binary files
- 1 HDF5 file

All files are properly detected and loaded by mcnptoolspro.

## File Naming Convention

Files are named with format suffixes for easy identification:
- `*_ASC.*` - ASCII format files
- `*_BIN.*` - Binary (Fortran) format files
- `*_HDF5.*` - HDF5 format files

## Test Coverage

### ASCII Files (13)
All filter types are covered for both MCNP 6.2 and 6.3:

**MCNP 6.2 filters:**
- `ptrac_filter_all_ASC.ip` - All filter types combined
- `ptrac_filter_event_ASC.ip` - Event-based filtering
- `ptrac_filter_filter_ASC.ip` - Custom filter
- `ptrac_filter_none_ASC.ip` - No filtering
- `ptrac_filter_tally_ASC.ip` - Tally-based filtering
- `ptrac_filter_type_ASC.ip` - Particle type filtering

**MCNP 6.3 filters:**
- `ptrac63_filter_all_ASC.ip` - All filter types combined
- `ptrac63_filter_event_ASC.ip` - Event-based filtering
- `ptrac63_filter_filter_ASC.ip` - Custom filter
- `ptrac63_filter_none_ASC.ip` - No filtering
- `ptrac63_filter_tally_ASC.ip` - Tally-based filtering
- `ptrac63_filter_type_ASC.ip` - Particle type filtering

**Basic example:**
- `basic_ptrac_example_ASC.ptrac` - Standard ASCII PTRAC file (20 MB)

### Binary Files (4)
- `example_ptrac_1_BIN.ptrac` - Basic binary PTRAC
- `example_ptrac_2_BIN.ptrac` - Binary PTRAC variant
- `LB6411_cezane_SC_75_BIN.ip` - Production simulation
- `LB6411_cezane_event_BIN.ptrac` - Event filtering in binary format

### HDF5 Files (1)
- `example_ptrac_3_HDF5.h5` - HDF5 format example (468 KB)

## Testing

To test all files:
```bash
python examples/test_all_ptrac_files.py
```

Or test individual files:
```python
import mcnptoolspro as mtp

# ASCII file
ptrac = mtp.Ptrac('tests/test_data_github/ptrac_filter_all_ASC.ip', mtp.Ptrac.ASC_PTRAC)
histories = ptrac.ReadHistories(5)

# Binary file
ptrac = mtp.Ptrac('tests/test_data_github/example_ptrac_1_BIN.ptrac', mtp.Ptrac.BIN_PTRAC)
histories = ptrac.ReadHistories(5)

# HDF5 file
ptrac = mtp.Ptrac('tests/test_data_github/example_ptrac_3_HDF5.h5', mtp.Ptrac.HDF5_PTRAC)
histories = ptrac.ReadHistories(5)
```

## Automatic Format Detection

Use the `detect_ptrac_mode()` utility for automatic format detection:
```python
from tools.sandbox import detect_ptrac_mode
import mcnptoolspro as mtp

filepath = 'tests/test_data_github/example_ptrac_1_BIN.ptrac'
mode = detect_ptrac_mode(filepath)  # Returns 'BIN_PTRAC'
ptrac = mtp.Ptrac(filepath, getattr(mtp.Ptrac, mode))
```

## File Sizes

- ASCII files: 211 KB - 20 MB
- Binary files: 1.4 MB each
- HDF5 file: 468 KB

Total size: ~30 MB
