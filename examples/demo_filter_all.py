"""
Demo: Reading PTRAC with COMBINED filters (all)

This example shows how to read a PTRAC file with MULTIPLE filters combined.
This is the most aggressive filtering, resulting in maximum file size reduction.

MCNP Input: ptrac event=src,bnk,ter type=n,h,t tally=4 filter=100
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def main():
    print("=" * 70)
    print("DEMO: PTRAC with COMBINED FILTERS")
    print("=" * 70)
    print()

    test_file = Path(__file__).parent.parent / 'tests' / 'test_data' / 'ptrac_filter_all.ip'

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
    print("FILTERS APPLIED:")
    print("  - event=src,bnk,ter  (only source, bank, termination events)")
    print("  - type=n,h,t         (only neutrons, protons, tritons)")
    print("  - tally=4            (only particles contributing to tally 4)")
    print("  - filter=100         (only particles crossing surface 100)")
    print()
    print("This is the MAXIMUM filtering - particles must satisfy ALL conditions!")
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

        if num_events > 0:
            print(f"  - Events (all pass combined filter):")
            for j in range(num_events):
                event = hist.GetEvent(j)
                event_type = event.Type()
                print(f"    Event {j+1}: Type={event_type}")
        else:
            print(f"  - No events (particle did not satisfy all filter criteria)")

        print()

    print("-" * 70)
    print(f"SUMMARY:")
    print(f"  Total histories: {len(histories)}")
    print(f"  Total events: {total_events}")
    print()
    print("FILTER COMPARISON:")
    print(f"  Baseline (no filter):  63 events (100%)")
    print(f"  Event filter only:      9 events ( 14%)")
    print(f"  Type filter only:      13 events ( 21%)")
    print(f"  Filter (surface) only: 15 events ( 24%)")
    print(f"  Tally filter only:    319 events (506%)")
    print(f"  COMBINED (all):        {total_events:2} events ({total_events/63*100:4.1f}%)")
    print()
    print("FILE SIZE REDUCTION:")
    print(f"  Combined filters reduce file size by ~{(1 - total_events/63)*100:.0f}%!")
    print()
    print("KEY INSIGHT:")
    print("  When filters are combined (AND logic), only particles satisfying")
    print("  ALL criteria are recorded. This gives maximum compression.")
    print()
    print("  This is what mcnptoolspro fixes - the original mcnptools")
    print("  would FAIL or enter infinite loop with combined filters!")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
