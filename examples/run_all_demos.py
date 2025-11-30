"""
Run all filter demos in sequence

This script runs all demo examples to show mcnptoolspro capabilities.
Perfect for first-time users to see concrete results!
"""

import sys
from pathlib import Path

# Import all demo scripts
demos = [
    ('demo_filter_none.py', 'No Filter (Baseline)'),
    ('demo_filter_event.py', 'Event Filter (src, bnk, ter)'),
    ('demo_filter_type.py', 'Type Filter (n, h, t)'),
    ('demo_filter_filter.py', 'Filter Card (position/angle/energy)'),
    ('demo_filter_tally.py', 'Tally Filter (tally=4)'),
    ('demo_filter_all.py', 'Combined Filters (ALL)'),
]


def run_demo(demo_file, description):
    """Run a single demo script"""
    print()
    print("=" * 76)
    print()
    print(description.center(76))
    print()
    print("=" * 76)
    print()

    demo_path = Path(__file__).parent / demo_file

    if not demo_path.exists():
        print(f"ERROR: Demo file not found: {demo_file}")
        return False

    # Execute demo by importing and calling main()
    try:
        # Create a namespace for the demo
        namespace = {
            '__name__': '__main__',
            '__file__': str(demo_path),
            'sys': sys,
            'Path': Path,
        }

        # Read and compile the demo code
        with open(demo_path, 'r') as f:
            code = compile(f.read(), str(demo_path), 'exec')

        # Execute the code in the namespace
        exec(code, namespace)

        # Call the main function if it exists
        if 'main' in namespace:
            result = namespace['main']()
            return result == 0
        else:
            return True

    except SystemExit:
        # Ignore sys.exit() calls from demos
        return True
    except Exception as e:
        print(f"ERROR running {demo_file}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print()
    print("=" * 76)
    print()
    print("mcnptoolspro - INTERACTIVE DEMO SUITE".center(76))
    print()
    print("Run all filter demonstrations to see how mcnptoolspro".center(76))
    print("correctly handles filtered PTRAC files!".center(76))
    print()
    print("=" * 76)
    print()

    input("Press ENTER to start demos...")

    results = []
    for demo_file, description in demos:
        success = run_demo(demo_file, description)
        results.append((description, success))

        if demo_file != demos[-1][0]:  # Not last demo
            print()
            input("Press ENTER for next demo...")

    # Summary
    print()
    print()
    print("=" * 76)
    print()
    print("DEMO SUMMARY".center(76))
    print()
    print("=" * 76)
    print()

    for description, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {status:8} {description}")

    print()
    passed = sum(1 for _, s in results if s)
    total = len(results)

    if passed == total:
        print(f"  All demos passed ({passed}/{total})!")
        print()
        print("  mcnptoolspro is working correctly on your system.")
        print("  You can now use it for your own PTRAC files!")
    else:
        print(f"  Some demos failed ({passed}/{total} passed)")
        print("  Check error messages above for details.")

    print()
    print("=" * 76)

    return 0 if passed == total else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(1)
