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

### `test_data/` Directory

Contains 6 sample PTRAC files (ASCII format, MCNP 6.2):

| File | Description | Events |
|------|-------------|--------|
| `ptrac_filter_none.ip` | No filter (baseline) | 63 |
| `ptrac_filter_event.ip` | Event filter (src, bnk, ter) | 9 |
| `ptrac_filter_type.ip` | Type filter (n, h, t) | 13 |
| `ptrac_filter_filter.ip` | Surface filter | 15 |
| `ptrac_filter_tally.ip` | Tally filter | 319 |
| `ptrac_filter_all.ip` | Combined filters | 2 |

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

1. Add test PTRAC file to `test_data/`
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

## Known Issues

- Tests currently validate ASCII format only
- Binary and HDF5 formats not yet tested
- MCNP 6.3 compatibility not verified

See [../TODO.md](../TODO.md) for planned testing improvements.
