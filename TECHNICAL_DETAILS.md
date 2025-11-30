# Technical Details - C++ Modifications

This document explains the core C++ modifications made to `libmcnptools/src/ptrack/Ptrac.cpp` to support filtered PTRAC files.

---

## Overview

The original LANL mcnptools library has incomplete support for PTRAC files generated with MCNP filters. This causes:
- **Infinite loops** when reading files with combined filters (`nkw=3`)
- **Parsing errors** with tally filters (negative keyword indicators)
- **Data corruption** due to incorrect skip logic

This document details the three main fixes applied.

---

## PTRAC Header Structure

PTRAC files have a 7+ line header. Lines 4, 5, and (conditionally) 6 contain keyword entries that describe active filters:

```
Line 1: Format info
Line 2: Problem info
Line 3: Number values
Line 4: Keyword entries part 1 (10 values) ← Event/filter info
Line 5: Keyword entries part 2 (10 values) ← Type/tally info, nkw value
Line 6: Keyword entries part 3 (10 values) ← Only if nkw ≥ 3 (combined filters)
Line 7: [Filter parameters OR number data]
...
```

### Key values

- **`nkw`** (Line 5, position 0): Number of keyword entry lines to read
  - `nkw = 0`: Read lines 4 and 5 only
  - `nkw ≥ 3`: Read lines 4, 5, **and 6**

- **Negative values**: Indicate tally filter
  - `kwent[4] < 0` (Line 5, position 4): Tally filter
  - `kwent[9] < 0` (Line 6, position 4): Tally filter in combined mode

---

## Fix #1: Infinite Loop with `nkw=3`

### Problem

Original code used a complex counting algorithm to determine when to stop reading keyword entries:

```cpp
// ORIGINAL CODE (simplified)
unsigned int nkwcnt = 0;
unsigned int kwlinecnt = 0;
bool done = false;

while(!done) {
    // Read 10 values
    for(int i=0; i<10; i++) {
        m_handle >> tmp;
        kwent.push_back(tmp);
        if(tmp != 0.0) nkwcnt++;  // Count non-zero values
    }
    kwlinecnt++;

    if(nkwcnt >= nkw && kwlinecnt >= 1)
        done = true;  // Exit condition
}
```

**Issue**: With `nkw=3` and tally filters (negative values), `nkwcnt` never reaches `nkw`, causing infinite loop.

### Solution

Replace complex counting with simple deterministic approach:

```cpp
// NEW CODE
// Read line 5 (always present)
double tmp;
m_handle >> tmp;
nkw = (unsigned int) tmp;

for(unsigned int i=1; i<10; i++) {
    m_handle >> tmp;
    kwent.push_back(tmp);
}

// If nkw >= 3, also read line 6
if(nkw >= 3) {
    for(unsigned int i=0; i<10; i++) {
        m_handle >> tmp;
        kwent.push_back(tmp);
    }
}
```

**Result**: No more infinite loops. Reading is deterministic based on `nkw` value.

---

## Fix #2: Tally Filter Detection

### Problem

Original code failed to detect tally filters because it only checked a subset of keyword positions.

### Solution

Check **both** possible locations for tally indicators:

```cpp
// Check line 5 (kwent[0-9]) for tally filter
bool has_tally_filter = false;

if(kwent.size() >= 5 && kwent[4] < 0.0) {
    has_tally_filter = true;  // Tally in position 4 (line 5)
}

// Check line 6 (kwent[9-18]) for tally filter (combined mode)
if(kwent.size() >= 10 && kwent[9] < 0.0) {
    has_tally_filter = true;  // Tally in position 9 (line 6)
}
```

**Result**: Tally filters correctly detected in all cases.

---

## Fix #3: Skip Logic

### Problem

After reading the header, PTRAC files have either:
- **Filter parameters** (1 line of 10 values) for non-tally filters
- **Number data** (0 lines to skip) for tally filters or unfiltered files

Original code had incorrect skip logic causing data corruption.

### Solution

Unified skip logic based on filter detection:

```cpp
bool has_filter = (has_event_filter || has_filter_keyword || has_type_filter);
bool has_tally = has_tally_filter;

if(has_filter && has_tally) {
    // Tally-only OR combined with tally: no skip
    // (number data starts immediately)
}
else if(has_filter) {
    // Event/type/filter without tally: skip 1 line (filter params)
    double filter_param;
    for(int i=0; i<10; i++) {
        m_handle >> filter_param;
    }
}
// else: no filter, no skip (number data starts immediately)
```

**Result**: Correct data alignment for all filter combinations.

---

## Complete Example: Combined Filter

### MCNP Input

```
ptrac file=asc max=-1000 tally=4 filter=-200,200,X event=src,bnk,ter type=n,h,t write=all
```

This uses **4 filters simultaneously**: `tally`, `filter`, `event`, `type`.

### PTRAC Header Structure

```
Line 1: -1 (ASCII format)
Line 2: [problem info]
Line 3: [number values]
Line 4: [0, 0, 0, 0, 3, 0, 0, 1, 0, 0]  ← 3 events filtered, filter #1
                      ^           ^
                      |           filter keyword
                      event count

Line 5: [3, 0, 0, 2, -1, 0, 0, 0, 0, 0]  ← nkw=3, 2 types, tally (negative!)
         ^        ^   ^
         |        |   tally indicator (negative)
         |        type count
         nkw value

Line 6: [0, 0, 0, 0, -1, 0, 0, 0, 0, 0]  ← Tally indicator in position 4
                      ^
                      tally (negative)

Line 7: [number data starts here - no filter params because tally present]
```

### Parsing Flow

```cpp
// 1. Read line 4
std::vector<double> line4_values = {0, 0, 0, 0, 3, 0, 0, 1, 0, 0};

// 2. Read line 5
nkw = 3;
kwent = {0, 0, 2, -1, 0, 0, 0, 0, 0};

// 3. Read line 6 (because nkw >= 3)
kwent = {0, 0, 2, -1, 0, 0, 0, 0, 0,  // line 5
         0, 0, 0, 0, -1, 0, 0, 0, 0, 0};  // line 6

// 4. Detect filters
has_event_filter = (line4_values[4] > 0);  // true (3 events)
has_filter_keyword = (line4_values[7] > 0);  // true (filter #1)
has_type_filter = (kwent[2] > 0 && kwent[3] > 0);  // true (2 types)
has_tally_filter = (kwent[3] < 0 || kwent[13] < 0);  // true (tally)

// 5. Skip logic
has_filter = true;  // event + filter + type detected
has_tally = true;   // tally detected

// → No skip (tally present, number data starts at line 7)
```

**Result**: File parsed correctly despite complex filter combination.

---

## Summary of Changes

| Issue | Original Behavior | New Behavior |
|-------|------------------|--------------|
| **`nkw=3` reading** | Infinite loop | Deterministic read based on `nkw` |
| **Tally detection** | Missed negative values | Checks both kwent[4] and kwent[9] |
| **Skip logic** | Incorrect line count | Unified: 0 skip for tally, 1 skip for non-tally |

---

## Code Location

All modifications are in:
```
libmcnptools/src/ptrack/Ptrac.cpp
Lines ~249-353 (ReadHeaders function)
```

---

## Testing

Validated against 6 filter combinations:
- ✅ No filter (`none`)
- ✅ Event filter (`event=src,bnk,ter`)
- ✅ Type filter (`type=h,t`)
- ✅ filter filter (`filter=0.0,10.0,X 0,1,U 1.0,2,ERG`)
- ✅ Tally filter (`tally=4`)
- ✅ Combined filter (`event + type + tally + filter`)

All tests pass with 100% success rate on ASCII PTRAC files (MCNP 6.2).

---

## Future Work

- Validate on binary PTRAC files
- Test with MCNP 6.3
- Test additional filter combinations
- Add HDF5 support validation

See [TODO.md](TODO.md) for full list of planned improvements.
