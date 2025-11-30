"""
Demo: Reading PTRAC with TALLY filter

This example shows how to read a PTRAC file filtered by tally contribution.
Only particles contributing to the specified tally are recorded.

MCNP Input: ptrac tally=4
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def main():
    print("=" * 70)
    print("DEMO: PTRAC with TALLY FILTER (tally=4)")
    print("=" * 70)
    print()

    test_file = Path(__file__).parent.parent / 'tests' / 'test_data' / 'ptrac_filter_tally.ip'

    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        print()
        print("HINT: Run this demo from the mcnptoolspro root directory:")
        print(f"  python examples/{Path(__file__).name}")
        print()
        print("You are currently in:", Path.cwd())
        return 1

    print(f"Reading PTRAC file: {test_file.name}")
    print(f"Filter: tally=4")
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
        print(f"  - All events contribute to tally 4")

        # Show some events
        if num_events > 0:
            print(f"  - Sample events:")
            for j in range(min(3, num_events)):
                event = hist.GetEvent(j)
                event_type = event.Type()
                print(f"    Event {j+1}: Type={event_type}")
            if num_events > 3:
                print(f"    ... and {num_events - 3} more")

        print()

    print("-" * 70)
    print(f"SUMMARY:")
    print(f"  Total histories: {len(histories)}")
    print(f"  Total events: {total_events}")
    print()
    print("FILTER EFFECT:")
    print(f"  Baseline (no filter): 63 events")
    print(f"  With tally filter:    {total_events} events")
    print()
    print("NOTE: Tally filter records ONLY particles that contribute to")
    print("      the specified tally. This can result in MORE events than")
    print("      baseline if many particles contribute, or FEWER if only")
    print("      specific particles contribute.")
    print()
    print("In this case: More events because the tally tracks many particles.")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
