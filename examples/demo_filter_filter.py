"""
Demo: Reading PTRAC with FILTER (position/angle/energy filter)

This example shows how to read a PTRAC file with a filter card.
Filter used: writes only events where:
- particle's x-coordinate is between 0 and 10 cm
- particle's x-axis cosine is between 0 and 1
- particle's energy is between 1 and 2 MeV

MCNP Input: ptrac filter=...
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def main():
    print("=" * 70)
    print("DEMO: PTRAC with FILTER (position/angle/energy)")
    print("=" * 70)
    print()

    test_file = Path(__file__).parent.parent / 'tests' / 'test_data_github' / 'ptrac_filter_filter_ASC.ip'

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
    print("FILTER CONDITIONS:")
    print("  - x-coordinate: 0 to 10 cm")
    print("  - x-axis cosine: 0 to 1")
    print("  - Energy: 1 to 2 MeV")
    print()
    print("Only particles satisfying ALL conditions are recorded.")
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
        print(f"  - First {min(num_events, 3)} events:")
        for j in range(min(num_events, 3)):
            event = hist.GetEvent(j)
            print(f"    Event {j+1}: Type={event.Type()}")

        print()

    print("-" * 70)
    print(f"SUMMARY:")
    print(f"  Total histories: {len(histories)}")
    print(f"  Total events: {total_events}")
    print()
    print("FILTER EFFECT:")
    print(f"  Baseline (no filter):    63 events")
    print(f"  With position/E filter:  {total_events} events")
    print(f"  Reduction: {(1 - total_events/63)*100:.1f}%")
    print()
    print("NOTE: Filter card allows complex spatial, angular, and energy")
    print("      selection criteria for particle tracking.")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
