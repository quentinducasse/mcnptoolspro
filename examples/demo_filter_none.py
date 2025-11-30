"""
Demo: Reading PTRAC with NO filter (baseline)

This example shows how to read a PTRAC file without any filters.
All particle events are recorded.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def main():
    print("=" * 70)
    print("DEMO: PTRAC with NO FILTER (baseline)")
    print("=" * 70)
    print()

    # Path to test file
    test_file = Path(__file__).parent.parent / 'tests' / 'test_data' / 'ptrac_filter_none.ip'

    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        print()
        print("HINT: Run this demo from the mcnptoolspro root directory:")
        print(f"  python examples/{Path(__file__).name}")
        print()
        print("You are currently in:", Path.cwd())
        return 1

    print(f"Reading PTRAC file: {test_file.name}")
    print()

    # Open PTRAC file
    ptrac = m.Ptrac(str(test_file), m.Ptrac.ASC_PTRAC)

    # Read histories
    print("Reading first 2 particle histories...")
    histories = ptrac.ReadHistories(2)

    print(f"Successfully read {len(histories)} histories")
    print()

    # Analyze each history
    total_events = 0
    for i, hist in enumerate(histories, 1):
        num_events = hist.GetNumEvents()
        total_events += num_events

        print(f"History {i}:")
        print(f"  - Number of events: {num_events}")

        # Show first few events
        print(f"  - First 3 events:")
        for j in range(min(3, num_events)):
            event = hist.GetEvent(j)
            event_type = event.Type()
            print(f"    Event {j+1}: Type={event_type}")

        print()

    print("-" * 70)
    print(f"SUMMARY:")
    print(f"  Total histories: {len(histories)}")
    print(f"  Total events: {total_events}")
    print(f"  Average events per history: {total_events / len(histories):.1f}")
    print()
    print("NOTE: Without filters, ALL particle events are recorded.")
    print("      This is the baseline - maximum file size.")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
