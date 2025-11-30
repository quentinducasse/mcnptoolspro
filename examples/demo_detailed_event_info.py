"""
Demo: Detailed Event Information

This script displays complete information about all events in the first history
of a PTRAC file, including position, direction, energy, weight, etc.

Usage:
    python demo_detailed_event_info.py [ptrac_file]

If no file is specified, uses ptrac_filter_none.ip by default.

Examples:
    python demo_detailed_event_info.py                                       # No filter (63 events)
    python demo_detailed_event_info.py ../tests/test_data/ptrac_filter_none.ip
    python demo_detailed_event_info.py ../tests/test_data/ptrac_filter_event.ip   # Event filter (9 events)
    python demo_detailed_event_info.py ../tests/test_data/ptrac_filter_type.ip    # Type filter (13 events)
    python demo_detailed_event_info.py ../tests/test_data/ptrac_filter_filter.ip  # Filter card (15 events)
    python demo_detailed_event_info.py ../tests/test_data/ptrac_filter_tally.ip   # Tally filter (319 events)
    python demo_detailed_event_info.py ../tests/test_data/ptrac_filter_all.ip     # Combined (2 events)
"""

import sys
from pathlib import Path
from collections import OrderedDict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))

import mcnptoolspro as m

# Event type labels
event_base_labels = {
    1000: "SRC", 2000: "BNK", 3000: "SUR", 4000: "COL", 5000: "TER", 9000: "LST"
}

# PTRAC data field codes
ptrac_data_fields = OrderedDict([
    (1, "NPS"), (2, "FIRST_EVENT_TYPE"), (3, "NPSCELL"), (4, "NPSSURFACE"),
    (5, "TALLY"), (6, "VALUE"), (7, "NEXT_EVENT_TYPE"), (8, "NODE"), (9, "NSR"),
    (10, "ZAID"), (11, "RXN"), (12, "SURFACE"), (13, "ANGLE"), (14, "TERMINATION_TYPE"),
    (15, "BRANCH"), (16, "PARTICLE"), (17, "CELL"), (18, "MATERIAL"),
    (19, "COLLISION_NUMBER"), (20, "X"), (21, "Y"), (22, "Z"),
    (23, "U"), (24, "V"), (25, "W"), (26, "ENERGY"), (27, "WEIGHT"),
    (28, "TIME"), (29, "SOURCE_TYPE"), (30, "BANK_TYPE")
])

# Particle type labels
particle_labels = {
    1: "NEUTRON", 2: "PHOTON", 3: "ELECTRON", 4: "POSITRON",
    5: "PROTON", 6: "DEUTERON", 7: "TRITON", 8: "HELIUM3",
    9: "ALPHA", 10: "HEAVY_ION", 11: "CHARGED", 12: "NEUTRAL"
}


def print_event_details(event, event_num):
    """Print detailed information about a single event"""
    evt_type = event.Type()
    base_code = (evt_type // 1000) * 1000
    base_label = event_base_labels.get(base_code, f"UNKNOWN({evt_type})")

    print(f"\n  ========== Event #{event_num}: {base_label} (type {evt_type}) ==========")

    # Print all available fields
    for field_code, field_label in ptrac_data_fields.items():
        if event.Has(field_code):
            try:
                val = event.Get(field_code)

                # Format specific fields
                if field_label == "PARTICLE":
                    particle_name = particle_labels.get(int(val), f"UNKNOWN({int(val)})")
                    print(f"    {field_label:20s} = {int(val):3d} ({particle_name})")
                elif field_label in ["X", "Y", "Z", "U", "V", "W", "ENERGY", "WEIGHT", "TIME"]:
                    print(f"    {field_label:20s} = {val:.6e}")
                elif field_label in ["CELL", "SURFACE", "MATERIAL", "COLLISION_NUMBER"]:
                    print(f"    {field_label:20s} = {int(val)}")
                else:
                    print(f"    {field_label:20s} = {val}")
            except Exception as e:
                print(f"    {field_label:20s} = [ERROR: {e}]")


def main():
    print("=" * 80)
    print("DEMO: DETAILED EVENT INFORMATION")
    print("=" * 80)
    print()

    # Determine which file to use
    if len(sys.argv) > 1:
        ptrac_file = Path(sys.argv[1])
        if not ptrac_file.is_absolute():
            # If relative path, make it relative to current directory
            ptrac_file = Path.cwd() / ptrac_file
    else:
        # Default file
        ptrac_file = Path(__file__).parent.parent / 'tests' / 'test_data' / 'ptrac_filter_none.ip'

    if not ptrac_file.exists():
        print(f"ERROR: File not found: {ptrac_file}")
        print()
        print("Usage:")
        print(f"  python {Path(__file__).name} [ptrac_file]")
        print()
        print("Examples:")
        print(f"  python {Path(__file__).name}                                       # No filter (63 events)")
        print(f"  python {Path(__file__).name} ../tests/test_data/ptrac_filter_none.ip")
        print(f"  python {Path(__file__).name} ../tests/test_data/ptrac_filter_event.ip   # Event filter (9 events)")
        print(f"  python {Path(__file__).name} ../tests/test_data/ptrac_filter_type.ip    # Type filter (13 events)")
        print(f"  python {Path(__file__).name} ../tests/test_data/ptrac_filter_filter.ip  # Filter card (15 events)")
        print(f"  python {Path(__file__).name} ../tests/test_data/ptrac_filter_tally.ip   # Tally filter (319 events)")
        print(f"  python {Path(__file__).name} ../tests/test_data/ptrac_filter_all.ip     # Combined (2 events)")
        return 1

    print(f"Reading PTRAC file: {ptrac_file.name}")
    print(f"Full path: {ptrac_file}")
    print()

    # Open PTRAC file
    try:
        ptrac = m.Ptrac(str(ptrac_file), m.Ptrac.ASC_PTRAC)
    except Exception as e:
        print(f"ERROR opening PTRAC file: {e}")
        return 1

    # Read first history
    print("Reading first particle history...")
    try:
        histories = ptrac.ReadHistories(1)
    except Exception as e:
        print(f"ERROR reading histories: {e}")
        return 1

    if len(histories) == 0:
        print("ERROR: No histories found in file")
        return 1

    hist = histories[0]
    num_events = hist.GetNumEvents()

    print(f"Successfully read history with {num_events} events")
    print()

    print("=" * 80)
    print(f"HISTORY 1 - DETAILED EVENT INFORMATION ({num_events} events)")
    print("=" * 80)

    # Print details for each event
    for i in range(num_events):
        try:
            event = hist.GetEvent(i)
            print_event_details(event, i + 1)
        except Exception as e:
            print(f"\n  Event #{i+1}: ERROR - {e}")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  File:          {ptrac_file.name}")
    print(f"  Total events:  {num_events}")
    print()
    print("NOTE: This demo shows ALL available fields for each event.")
    print("      Field codes follow MCNP PTRAC format specification.")
    print("      - Position: X(20), Y(21), Z(22) in cm")
    print("      - Direction: U(23), V(24), W(25) cosines")
    print("      - Energy: ENERGY(26) in MeV")
    print("      - Weight: WEIGHT(27)")
    print("      - Time: TIME(28) in shakes")
    print("=" * 80)

    return 0


if __name__ == '__main__':
    sys.exit(main())
