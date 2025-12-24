#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTRAC file format detection utilities
Based on DECIMA_v2 robust 3-level detection strategy
"""

import os


def detect_ptrac_mode(ptrac_path):
    """
    Automatically detect the format of a PTRAC file using a 3-level strategy:

    1. HDF5 detection (extension .h5/.hdf5 OR magic bytes)
    2. Fortran binary markers detection (size1 == size2)
    3. ASCII content analysis (ratio + keywords)

    UNIVERSAL: Works with ANY file extension (.ptrac, .p, .ip, .bin, .txt, etc.)
    Only HDF5 uses extension hints - all other formats rely on CONTENT analysis.

    Args:
        ptrac_path (str): Path to the PTRAC file

    Returns:
        str: 'HDF5_PTRAC', 'BIN_PTRAC', or 'ASC_PTRAC'
    """
    try:
        # === Level 1: HDF5 detection (only reliable extension shortcut) ===
        filename_lower = os.path.basename(ptrac_path).lower()

        # HDF5 extension hint (will be confirmed by magic bytes)
        if '.h5' in filename_lower or filename_lower.endswith('.hdf5'):
            return 'HDF5_PTRAC'

        # === Level 2: Magic bytes detection ===
        with open(ptrac_path, "rb") as f:
            header = f.read(512)

        # HDF5 magic signature (8 bytes)
        if len(header) >= 8 and header[:8] == b'\x89HDF\r\n\x1a\n':
            return 'HDF5_PTRAC'

        # === Level 3: Content analysis ===
        # Strategy: Check for Fortran binary markers FIRST (more reliable)
        # Then fall back to ASCII detection

        # Check for Fortran binary record markers
        if len(header) >= 8:
            try:
                # First 4 bytes = record size, should match after record
                size1 = int.from_bytes(header[0:4], byteorder='little')
                if 0 < size1 < 10000:  # Reasonable header size
                    # Check if size2 matches (Fortran record end marker)
                    if len(header) >= 8 + size1:
                        size2 = int.from_bytes(header[4+size1:8+size1], byteorder='little')
                        if size1 == size2:
                            # Valid Fortran binary format detected
                            return 'BIN_PTRAC'
            except:
                pass

        # If no clear binary markers, check for ASCII content
        ascii_count = 0
        for byte in header[:256]:
            # Printable ASCII or whitespace
            if (32 <= byte <= 126) or byte in (9, 10, 13):  # tab, LF, CR
                ascii_count += 1

        ascii_ratio = ascii_count / min(256, len(header))

        # High ASCII ratio (>95%) = ASCII PTRAC
        if ascii_ratio > 0.95:
            return 'ASC_PTRAC'

        # Lower threshold (>85%) + PTRAC keywords = ASCII PTRAC
        if ascii_ratio > 0.85:
            try:
                text_sample = header[:256].decode('ascii', errors='ignore').lower()
                if 'ptrac' in text_sample or 'nps' in text_sample or 'mcnp' in text_sample:
                    return 'ASC_PTRAC'
            except:
                pass

        # Ambiguous case: default to BINARY (safer for Fortran files)
        return 'BIN_PTRAC'

    except Exception:
        # Fallback: assume ASCII (safest default for text-based errors)
        return 'ASC_PTRAC'
