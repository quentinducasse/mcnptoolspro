# mcnptoolspro Tests

This directory contains tests for mcnptoolspro.

---

## Test Files

### Integration Tests

- **`test_all_filters.py`** - Tests all 6 filter types against sample PTRAC files
  - Validates filter combinations: none, event, type, filter, tally, all

### Unit Tests

- **`test_basic.py`** - Basic functionality tests
  - Import test
  - Object creation
  - Basic reading operations
  - Event data access

---

## Test Data

### `test_data_github/` Directory

Contains 18 comprehensive test files for public distribution:

**ASCII Files (13 files):**
- MCNP 6.2 filters: `ptrac_filter_*.ip` (all, event, filter, none, tally, type)
- MCNP 6.3 filters: `ptrac63_filter_*.ip` (all, event, filter, none, tally, type)
- Large example: `basic_ptrac_example_ASC.ptrac` (20 MB, production simulation)

**Binary Files (4 files):**
- `example_ptrac_1_BIN.ptrac` - Basic binary format
- `example_ptrac_2_BIN.ptrac` - Binary variant
- `LB6411_cezane_SC_75_BIN.ip` - Production simulation
- `LB6411_cezane_event_BIN.ptrac` - Event filtering in binary

**HDF5 Files (1 file):**
- `example_ptrac_3_HDF5.h5` - Modern HDF5 format

See [test_data_github/README.md](test_data_github/README.md) for complete documentation.

### Legacy `test_data/` Directory

Contains additional test files used during development (6 baseline + 43 extended files).
This directory is excluded from version control (.gitignore) and reserved for local testing.

---

## Running Tests

### Run all integration tests

```bash
cd mcnptoolspro/tests
python test_all_filters.py
```

Expected output:
```
Testing filter: none       ... OK (63 events)
Testing filter: event      ... OK (9 events)
Testing filter: type       ... OK (13 events)
Testing filter: filter     ... OK (15 events)
Testing filter: tally      ... OK (319 events)
Testing filter: all        ... OK (2 events)

All tests passed (6/6 filters)
```

### Run basic unit tests

```bash
python test_basic.py
```

Expected output:
```
[OK] Import mcnptoolspro
[OK] Ptrac constants accessible
[OK] Ptrac object creation
[OK] Read histories (2 histories, 33 events in first)
[OK] Event access (E=14.100 MeV, pos=(0.000, 0.000, 0.000))

All tests passed (5/5)
```

---

## Adding New Tests

### For new filter types

1. Add test PTRAC file to `test_data_github/` (with format suffix: _ASC, _BIN, _HDF5)
2. Add test case to `test_all_filters.py`
3. Update expected event counts

### For new functionality

1. Create new test file `test_<feature>.py`
2. Follow existing test structure
3. Update this README

---

## Test Requirements

- Python 3.7+
- mcnptoolspro installed (or in PYTHONPATH)
- Test data files in `test_data/`

---

## Comprehensive Testing

### Automated Test Suite

Run the comprehensive test suite on all 18 test files:

```bash
cd mcnptoolspro/examples
python test_all_ptrac_files.py
```

Expected output:
```
[STATS] OVERALL:
  Total files: 18
  SUCCESS: 18

[FILE] BY FORMAT:
  ASCII           | Total: 13 | OK: 13 | Failed:  0 | Timeout:  0
  BINARY          | Total:  4 | OK:  4 | Failed:  0 | Timeout:  0
  HDF5            | Total:  1 | OK:  1 | Failed:  0 | Timeout:  0
```

This validates:
- ✅ All three formats (ASCII, Binary, HDF5)
- ✅ All MCNP filter types (none, event, type, filter, tally, all)
- ✅ Both MCNP 6.2 and 6.3 compatibility
- ✅ Automatic format detection
- ✅ Performance (< 0.2s per file)

See [../TODO.md](../TODO.md) for future testing improvements.
