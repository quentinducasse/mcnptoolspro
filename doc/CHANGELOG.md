# Changelog

All notable changes to mcnptoolspro will be documented in this file.

## [Unreleased] - 2025-12-24

### Added
- **Complete Binary PTRAC Support** - All 8 binary test files now load successfully (100% success rate)
- **Format Auto-Detection** - New `tools.sandbox` module with `detect_ptrac_mode()` function
- **Comprehensive Test Suite** - `examples/test_all_ptrac_files.py` tests 50 PTRAC files with timeout protection
- **Binary Debug Tool** - `examples/debug_binary_ptrac.py` for low-level binary PTRAC analysis
- **Performance Metrics** - Test suite now reports load times and file size analysis
- **Documentation** - Added `tools/README.md` and `examples/README_TESTING.md`

### Fixed
- **Binary Filter Detection** - Disabled aggressive binary filter heuristic in `Ptrac.cpp:196` that caused false positives
  - Issue: Binary PTRAC files were incorrectly detected as filtered, causing parsing failures
  - Solution: Set `is_filtered_bin = false` to match DECIMA_v2 implementation
  - Impact: 8 binary files that previously failed now load successfully
- **Test Suite Path Resolution** - Fixed `test_all_ptrac_files.py` to correctly resolve `tests/test_data/` from any directory

### Changed
- **README.md** - Updated to reflect complete binary support and 98% test success rate
- **Key Improvements Section** - Added binary/HDF5 support, performance metrics
- **Testing Status Section** - Updated with comprehensive validation results (50 files)
- **Overview Section** - Added acknowledgment of LANL's excellent foundation work

## [5.3.1] - 2025-11-30

### Added
- Complete PTRAC filter support (tally, filter, event, type, combinations)
- MCNP 6.3 compatibility with special tally handling
- Interactive demo scripts for all filter types
- Comprehensive test suite for filtered PTRAC files

### Fixed
- Infinite loop with combined filters (nkw=3)
- Tally filter detection failure
- Incorrect skip logic for filtered files

### Changed
- Simplified header parsing for deterministic behavior
- Unified skip logic based on filter type

## Initial Release - 2025-11-01

### Added
- Fork from LANL mcnptools
- Enhanced PTRAC filter parsing
- Windows installation support with bundled HDF5
- Basic test suite and examples

---

## Version Numbering

mcnptoolspro follows the version numbering of the original mcnptools (currently 5.3.1) with enhancements documented in this changelog.
