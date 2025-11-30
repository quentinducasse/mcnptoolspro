# TODO - Future Improvements and Testing

## 🧪 Testing Priorities

### High Priority

- [ ] **Test with MCNP 6.3**
  - Verify PTRAC structure hasn't changed in MCNP 6.3
  - Validate all 6 filter types with MCNP 6.3 generated files
  - Document any differences from MCNP 6.2

- [ ] **Test binary PTRAC files**
  - Current testing is ASCII-only
  - Binary format may have different header structure
  - Validate filter detection works with binary format

- [ ] **Test HDF5 PTRAC files**
  - HDF5 format not yet validated
  - May require different parsing approach
  - Check if filters are handled similarly

### Medium Priority

- [ ] **Extended filter combination testing**
  - Test all possible 2-filter combinations
  - Test all possible 3-filter combinations
  - Test edge cases (empty filters, negative surface numbers, etc.)

- [ ] **Performance testing**
  - Benchmark large PTRAC files (>1GB)
  - Compare performance vs original mcnptools
  - Profile memory usage

- [ ] **Cross-platform validation**
  - Test on Linux (validated on Windows only so far)
  - Test on macOS
  - Verify endianness handling for binary files

### Low Priority

- [ ] **Additional MCNP versions**
  - Test with MCNP 5
  - Test with MCNPX
  - Document version-specific differences

- [ ] **Python API enhancements**
  - Add filter metadata extraction methods
  - Add convenience methods for common operations
  - Improve error messages

---

## 🐛 Known Issues

### To Investigate

- Some untested filter combinations may fail
- Binary/HDF5 format compatibility unknown
- MCNP 6.3 compatibility not verified

### Won't Fix (Upstream Issues)

- Issues inherited from original mcnptools that are unrelated to filters
- Refer to [LANL mcnptools issues](https://github.com/lanl/mcnptools/issues)

---

## ✨ Feature Requests

### Proposed

- [ ] Add filter information to Ptrac API
  - `ptrac.GetActiveFilters()` → list of active filters
  - `ptrac.GetFilterInfo()` → detailed filter metadata

- [ ] Add validation mode
  - `Ptrac(..., validate=True)` → extra checks during parsing
  - Helpful for debugging malformed PTRAC files

- [ ] Add Python-only version
  - Pure Python implementation for easier installation
  - May sacrifice performance for portability

---

## 📚 Documentation

### Needed

- [ ] Add more usage examples
- [ ] Create tutorial for common use cases
- [ ] Add troubleshooting section for filter-specific errors
- [ ] Document PTRAC header structure in detail

---

## 🔧 Development

### Build System

- [ ] Simplify CMake configuration
- [ ] Add precompiled wheels for common platforms
- [ ] Publish to PyPI for easy installation (`pip install mcnptoolspro`)

### Testing Infrastructure

- [ ] Add unit tests for individual functions
- [ ] Add GitHub Actions CI/CD (currently has workflow but not fully tested)
- [ ] Add code coverage reporting

---

## 📊 Metrics to Track

- Number of filter combinations tested
- Platforms validated (Windows, Linux, macOS)
- MCNP versions tested (6.2, 6.3, etc.)
- File formats validated (ASCII, binary, HDF5)

---

## 🤝 Community

### Contributions Welcome

If you can help with any of the above, please:
1. Open an issue to discuss
2. Fork the repository
3. Submit a pull request

Particularly needed:
- Access to MCNP 6.3 for testing
- Binary/HDF5 PTRAC file samples
- Linux/macOS testing results

---

**Last updated**: November 2025
