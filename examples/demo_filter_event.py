"""
Demo: Reading PTRAC with EVENT filter

This example shows how to read a PTRAC file filtered by event type.
Only specified events (src, bnk, ter) are recorded.

MCNP Input: ptrac event=src,bnk,ter
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m


def main():
    print("=" * 70)
    print("DEMO: PTRAC with EVENT FILTER (src, bnk, ter)")
    print("=" * 70)
    print()

    test_file = Path(__file__).parent.parent / 'tests' / 'test_data_github' / 'ptrac_filter_event_ASC.ip'

    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        print()
        print("HINT: Run this demo from the mcnptoolspro root directory:")
        print(f"  python examples/{Path(__file__).name}")
        print()
        print("You are currently in:", Path.cwd())
        return 1

    print(f"Reading PTRAC file: {test_file.name}")
    print(f"Filter: event=src,bnk,ter")
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
    event_types = {}

    for i, hist in enumerate(histories, 1):
        num_events = hist.GetNumEvents()
        total_events += num_events

        print(f"History {i}:")
        print(f"  - Number of events: {num_events}")

        # Count event types
        for j in range(num_events):
            event = hist.GetEvent(j)
            event_type = event.Type()
            event_types[event_type] = event_types.get(event_type, 0) + 1

        # Show some events
        print(f"  - Events recorded:")
        for j in range(min(num_events, 5)):
            event = hist.GetEvent(j)
            event_type = event.Type()
            print(f"    Event {j+1}: Type={event_type}")
        if num_events > 5:
            print(f"    ... and {num_events - 5} more")

        print()

    print("-" * 70)
    print(f"SUMMARY:")
    print(f"  Total histories: {len(histories)}")
    print(f"  Total events: {total_events}")
    print(f"  Event types recorded:")
    for event_type, count in sorted(event_types.items()):
        print(f"    {event_type}: {count} events")
    print()
    print("FILTER EFFECT:")
    print(f"  Baseline (no filter): 63 events")
    print(f"  With event filter:    {total_events} events")
    print(f"  Reduction: {(1 - total_events/63)*100:.1f}%")
    print()
    print("NOTE: Only SRC (source), BNK (bank), and TER (termination)")
    print("      events are recorded. Other events are excluded.")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
