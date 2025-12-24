#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worker process for testing individual PTRAC files.
This runs in a subprocess with timeout protection.
"""

import sys
import json
from pathlib import Path

if __name__ == '__main__':
    # Get arguments
    if len(sys.argv) < 3:
        print(json.dumps({'status': 'FAILED', 'error': 'Not enough arguments'}))
        sys.exit(1)

    filepath = Path(sys.argv[1])
    max_histories = int(sys.argv[2])
    project_root = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).parent.parent

    # Add project root to path
    sys.path.insert(0, str(project_root))

    try:
        # Import after adding to path
        from tools.sandbox import detect_ptrac_mode
        import mcnptoolspro as m

        # Detect format
        detected_mode = detect_ptrac_mode(str(filepath))

        if 'h5' in filepath.name.lower():
            format_type = 'HDF5'
            ptrac_mode = m.Ptrac.HDF5_PTRAC
        elif detected_mode == 'ASC_PTRAC':
            format_type = 'ASCII'
            ptrac_mode = m.Ptrac.ASC_PTRAC
        elif detected_mode == 'BIN_PTRAC':
            format_type = 'BINARY'
            ptrac_mode = m.Ptrac.BIN_PTRAC
        else:
            format_type = 'UNKNOWN'
            ptrac_mode = m.Ptrac.ASC_PTRAC

        # Try to open and read
        ptrac = m.Ptrac(str(filepath), ptrac_mode)
        histories = ptrac.ReadHistories(max_histories)

        events_count = 0
        if histories:
            first_hist = histories[0]
            events_count = first_hist.GetNumEvents()

        # Return success result as JSON
        result = {
            'status': 'SUCCESS',
            'format': format_type,
            'detected_mode': detected_mode,
            'histories_count': len(histories),
            'events_count': events_count,
            'error': None
        }
        print(json.dumps(result))

    except Exception as e:
        # Return error result as JSON
        result = {
            'status': 'FAILED',
            'format': 'UNKNOWN',
            'detected_mode': None,
            'histories_count': 0,
            'events_count': 0,
            'error': str(e)[:150]
        }
        print(json.dumps(result))
