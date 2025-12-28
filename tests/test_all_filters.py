"""
Integration test for all PTRAC filter types

Tests the 6 filter types supported by mcnptoolspro:
- none
- event
- type
- filter
- tally
- all (combined)
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def test_filter(filter_name, expected_events):
    """Test a single filter type"""
    # Path to test data
    test_file = Path(__file__).parent / 'test_data_github' / f'ptrac_filter_{filter_name}_ASC.ip'

    if not test_file.exists():
        print(f"Testing filter: {filter_name:10} ... SKIP (file not found)")
        return False

    try:
        # Read PTRAC file
        ptrac = m.Ptrac(str(test_file), m.Ptrac.ASC_PTRAC)
        histories = ptrac.ReadHistories(2)  # Read 2 histories (matching test data)

        # Count total events
        total_events = sum(hist.GetNumEvents() for hist in histories)

        # Check if matches expected
        if total_events == expected_events:
            print(f"Testing filter: {filter_name:10} ... OK ({total_events} events)")
            return True
        else:
            print(f"Testing filter: {filter_name:10} ... FAIL (expected {expected_events}, got {total_events})")
            return False

    except Exception as e:
        print(f"Testing filter: {filter_name:10} ... ERROR ({str(e)})")
        return False


def main():
    """Run all filter tests"""
    print("=" * 60)
    print("mcnptoolspro - Filter Integration Tests")
    print("=" * 60)
    print()

    # Define test cases: (filter_name, expected_event_count)
    test_cases = [
        ('none', 63),      # No filter - baseline
        ('event', 9),      # Event filter (src, bnk, ter)
        ('type', 13),      # Type filter (n, h, t)
        ('filter', 15),    # Surface filter
        ('tally', 319),    # Tally filter
        ('all', 2),        # Combined filter (event + type + tally + filter)
    ]

    results = []
    for filter_name, expected_events in test_cases:
        result = test_filter(filter_name, expected_events)
        results.append(result)

    print()
    print("=" * 60)

    # Summary
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"All tests passed ({passed}/{total} filters)")
        print("=" * 60)
        return 0
    else:
        print(f"Some tests failed ({passed}/{total} filters passed)")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
