"""
Basic unit tests for mcnptoolspro

Tests basic functionality:
- Import
- PTRAC object creation
- Basic reading
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'python'))


def test_import():
    """Test that mcnptoolspro can be imported"""
    try:
        import mcnptoolspro
        print("[OK] Import mcnptoolspro")
        return True
    except ImportError as e:
        print(f"[FAIL] Import mcnptoolspro: {e}")
        return False


def test_ptrac_constants():
    """Test that Ptrac constants are accessible"""
    try:
        import mcnptoolspro as m
        # Check that format constants exist
        assert hasattr(m.Ptrac, 'ASC_PTRAC'), "ASC_PTRAC constant missing"
        assert hasattr(m.Ptrac, 'BIN_PTRAC'), "BIN_PTRAC constant missing"
        print("[OK] Ptrac constants accessible")
        return True
    except (AssertionError, AttributeError) as e:
        print(f"[FAIL] Ptrac constants: {e}")
        return False


def test_ptrac_creation():
    """Test creating a Ptrac object"""
    try:
        import mcnptoolspro as m
        test_file = Path(__file__).parent / 'test_data_github' / 'ptrac_filter_none_ASC.ip'

        if not test_file.exists():
            print("[SKIP] Ptrac creation (test file not found)")
            return True

        ptrac = m.Ptrac(str(test_file), m.Ptrac.ASC_PTRAC)
        print("[OK] Ptrac object creation")
        return True

    except Exception as e:
        print(f"[FAIL] Ptrac creation: {e}")
        return False


def test_read_histories():
    """Test reading histories from PTRAC file"""
    try:
        import mcnptoolspro as m
        test_file = Path(__file__).parent / 'test_data_github' / 'ptrac_filter_none_ASC.ip'

        if not test_file.exists():
            print("[SKIP] Read histories (test file not found)")
            return True

        ptrac = m.Ptrac(str(test_file), m.Ptrac.ASC_PTRAC)
        histories = ptrac.ReadHistories(2)

        assert len(histories) > 0, "No histories read"
        assert histories[0].GetNumEvents() > 0, "No events in first history"

        print(f"[OK] Read histories ({len(histories)} histories, {histories[0].GetNumEvents()} events in first)")
        return True

    except Exception as e:
        print(f"[FAIL] Read histories: {e}")
        return False


def test_event_access():
    """Test accessing event data"""
    try:
        import mcnptoolspro as m
        test_file = Path(__file__).parent / 'test_data_github' / 'ptrac_filter_none_ASC.ip'

        if not test_file.exists():
            print("[SKIP] Event access (test file not found)")
            return True

        ptrac = m.Ptrac(str(test_file), m.Ptrac.ASC_PTRAC)
        histories = ptrac.ReadHistories(1)
        hist = histories[0]
        num_events = hist.GetNumEvents()

        assert num_events > 0, "No events accessible"

        # Check that we can access events
        first_event = hist.GetEvent(0)
        assert first_event is not None, "Event is None"

        print(f"[OK] Event access ({num_events} events accessible)")
        return True

    except Exception as e:
        print(f"[FAIL] Event access: {e}")
        return False


def main():
    """Run all basic tests"""
    print("=" * 60)
    print("mcnptoolspro - Basic Unit Tests")
    print("=" * 60)
    print()

    tests = [
        test_import,
        test_ptrac_constants,
        test_ptrac_creation,
        test_read_histories,
        test_event_access,
    ]

    results = [test() for test in tests]

    print()
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"All tests passed ({passed}/{total})")
        print("=" * 60)
        return 0
    else:
        print(f"Some tests failed ({passed}/{total} passed)")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
