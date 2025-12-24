# mcnptoolspro Examples

**Interactive demonstrations of PTRAC filter support**

This directory contains hands-on examples showing how mcnptoolspro reads filtered PTRAC files.

---

## Quick Start

**IMPORTANT**: Run all examples from the **project root directory**, not from `examples/`

### Run all demos (recommended for first-time users)

```bash
# From the mcnptoolspro root directory
python examples/run_all_demos.py
```

This will run all 6 demonstrations interactively, showing you concrete results for each filter type.

**Note**: If you see `ERROR: Test file not found`, make sure you're in the project root directory (`mcnptoolspro/`), not in `examples/`.

---

## Individual Demos

### 1. No Filter (Baseline)

```bash
# From the mcnptoolspro root directory
python examples/demo_filter_none.py
```

**Shows**: Baseline PTRAC with all events recorded (63 events)

**Output preview**:
```
History 1:
  - Number of events: 35
  - First 3 events:
    Event 1: Type=1000
    Event 2: Type=2000
    Event 3: Type=3000
```

---

### 2. Event Filter

```bash
# From the mcnptoolspro root directory
python examples/demo_filter_event.py
```

**MCNP input**: `ptrac event=src,bnk,ter`

**Shows**: Only source, bank, and termination events (9 events)

**Output preview**:
```
FILTER EFFECT:
  Baseline (no filter): 63 events
  With event filter:    9 events
  Reduction: 85.7%
```

---

### 3. Type Filter

```bash
# From the mcnptoolspro root directory
python examples/demo_filter_type.py
```

**MCNP input**: `ptrac type=n,h,t`

**Shows**: Only neutrons, protons, and tritons (13 events)

**Output preview**:
```
FILTER EFFECT:
  Baseline (no filter): 63 events
  With type filter:     13 events
  Reduction: 79.4%
```

---

### 4. Filter Card (position/angle/energy)

```bash
# From the mcnptoolspro root directory
python examples/demo_filter_filter.py
```

**MCNP input**: `ptrac filter=...`

**Shows**: Only particles satisfying spatial/angular/energy criteria (15 events)

**Filter conditions**:
- x-coordinate: 0 to 10 cm
- x-axis cosine: 0 to 1
- Energy: 1 to 2 MeV

**Output preview**:
```
FILTER EFFECT:
  Baseline (no filter):    63 events
  With position/E filter:  15 events
  Reduction: 76.2%
```

---

### 5. Tally Filter

```bash
# From the mcnptoolspro root directory
python examples/demo_filter_tally.py
```

**MCNP input**: `ptrac tally=4`

**Shows**: Only particles contributing to tally 4 (319 events)

**Output preview**:
```
NOTE: Tally filter records ONLY particles that contribute to
      the specified tally. This can result in MORE events than
      baseline if many particles contribute.
```

---

### 6. Combined Filters (Maximum reduction)

```bash
# From the mcnptoolspro root directory
python examples/demo_filter_all.py
```

**MCNP input**: `ptrac event=src,bnk,ter type=n,h,t tally=4 filter=100`

**Shows**: Combined filters - maximum file size reduction (2 events)

**Output preview**:
```
FILE SIZE REDUCTION:
  Combined filters reduce file size by ~97%!

KEY INSIGHT:
  This is what mcnptoolspro fixes - the original mcnptools
  would FAIL or enter infinite loop with combined filters!
```

---

## What You'll Learn

### From these demos you'll see:

1. **How filters reduce PTRAC file size**
   - Event filter: ~86% reduction
   - Combined filters: ~97% reduction

2. **Different filter behaviors**
   - Event filter: Fewer events (selective recording)
   - Tally filter: More events (tracks contributing particles)
   - Combined: Maximum reduction (AND logic)

3. **Real parsing results**
   - Actual event counts from sample files
   - Event types recorded
   - Filter effects visualized

4. **Why mcnptoolspro matters**
   - Original mcnptools fails with combined filters
   - mcnptoolspro handles all combinations correctly

---

## Requirements

- mcnptoolspro installed (or in PYTHONPATH)
- Test data files in `../tests/test_data/`

---

## Output Format

Each demo provides:
- ✅ Filter description
- ✅ Number of events recorded
- ✅ Sample event data
- ✅ Comparison with baseline
- ✅ File size reduction percentage
- ✅ Explanation of filter behavior

---

## Perfect For

- 🎓 **First-time users** - See concrete results immediately
- 🔬 **Researchers** - Understand filter effects on your data
- 🐛 **Debugging** - Verify mcnptoolspro installation
- 📚 **Learning** - Understand PTRAC filters interactively

---

## Next Steps

After running the demos:

1. **Use with your own PTRAC files**:
   ```python
   import mcnptoolspro as m
   ptrac = m.Ptrac('your_file.ptrac', m.Ptrac.ASC_PTRAC)
   histories = ptrac.ReadHistories(100)
   ```

2. **Run the test suite**:
   ```bash
   cd ../tests
   python test_all_filters.py
   ```

3. **Read the technical details**:
   - [TECHNICAL_DETAILS.md](../TECHNICAL_DETAILS.md)
   - [README.md](../README.md)

---

**Enjoy exploring mcnptoolspro!** 🚀

---

## Testing Scripts

### Comprehensive PTRAC Test Suite

```bash
# Test all PTRAC files in tests/test_data/
python examples/test_all_ptrac_files.py
```

**Features:**
- Tests ASCII, Binary, and HDF5 formats
- Auto-detects file format
- 5-second timeout per file (prevents hangs)
- Comprehensive statistics

**Expected output:**
```
Found 49 potential PTRAC files
[1/49] Testing: file1.ptrac [OK] 0.06s
...
SUCCESS: 49/49 files (100%)
  ASCII:  40/40 (100%)
  BINARY:  8/8  (100%)
  HDF5:    1/1  (100%)
```

### Debug Binary PTRAC

```bash
# Analyze binary PTRAC file structure
python examples/debug_binary_ptrac.py tests/test_data/file.ptrac
```

Shows low-level binary header structure for debugging.

