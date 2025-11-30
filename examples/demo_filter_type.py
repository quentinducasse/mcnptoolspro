"""
Demo: Reading PTRAC with TYPE filter

This example shows how to read a PTRAC file filtered by particle type.
Only specified particle types (n, h, t) are recorded.

MCNP Input: ptrac type=n,h,t
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def main():
    print("=" * 70)
    print("DEMO: PTRAC with TYPE FILTER (n, h, t)")
    print("=" * 70)
    print()

    test_file = Path(__file__).parent.parent / 'tests' / 'test_data' / 'ptrac_filter_type.ip'

    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        return 1

    print(f"Reading PTRAC file: {test_file.name}")
    print(f"Filter: type=n,h,t")
    print()
    print("This filter records only neutrons, protons, and tritons.")
    print("Other particle types are excluded.")
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
    print(f"  Baseline (no filter): 63 events")
    print(f"  With type filter:     {total_events} events")
    print(f"  Reduction: {(1 - total_events/63)*100:.1f}%")
    print()
    print("NOTE: Type filter reduces file size by excluding unwanted")
    print("      particle types (photons, electrons, etc.).")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
