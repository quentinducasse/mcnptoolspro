#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to load and analyze all PTRAC files in data/ptrac_samples/
This helps identify which files load correctly and which have issues.
With real per-file timeout using subprocess isolation.
"""

import sys
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_single_file_worker(filepath, max_histories):
    """Worker function to test a single file (runs in subprocess)"""
    try:
        # Import here to avoid issues in parent process
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


class PTRACTester:
    """Test PTRAC file loading with mcnptools using subprocess isolation"""

    # def __init__(self, base_dir="tests/test_data"):
    def __init__(self, base_dir="tests/test_data_github"):
        # If base_dir is relative, make it relative to project root
        self.base_dir = Path(base_dir)
        if not self.base_dir.is_absolute():
            self.base_dir = project_root / base_dir
        self.results = []
        self.timeout_seconds = 5  # 5 seconds timeout per file

    def get_file_size(self, filepath):
        """Get human-readable file size"""
        size_bytes = filepath.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def get_file_size_mb(self, filepath):
        """Get file size in MB as float"""
        return filepath.stat().st_size / (1024 * 1024)

    def test_file(self, filepath):
        """Test loading a single PTRAC file using subprocess with timeout"""
        result = {
            'file': filepath.name,
            'path': str(filepath),
            'size': self.get_file_size(filepath),
            'size_mb': self.get_file_size_mb(filepath),
            'format': 'UNKNOWN',
            'detected_mode': None,
            'status': 'UNKNOWN',
            'error': None,
            'histories_count': 0,
            'events_count': 0,
            'load_time': 0.0
        }

        # Note: .ip and .p files are also PTRAC files, not just MCNP input files

        # Adjust number of histories based on file size
        if result['size_mb'] > 50:
            max_histories = 2
        elif result['size_mb'] > 10:
            max_histories = 3
        else:
            max_histories = 5

        # Prepare subprocess command
        worker_script = project_root / 'examples' / '_test_worker.py'

        # Run in subprocess with timeout
        start_time = time.time()

        try:
            proc = subprocess.Popen(
                [sys.executable, str(worker_script), str(filepath), str(max_histories), str(project_root)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout, stderr = proc.communicate(timeout=self.timeout_seconds)
                result['load_time'] = time.time() - start_time

                # Parse JSON result
                try:
                    test_result = json.loads(stdout.strip().split('\n')[-1])
                    result.update(test_result)
                except (json.JSONDecodeError, IndexError):
                    # Failed to parse, check stderr
                    if 'mcnptoolspro' in stderr or 'ImportError' in stderr:
                        result['status'] = 'SKIPPED'
                        result['error'] = 'mcnptoolspro not available'
                    else:
                        result['status'] = 'FAILED'
                        result['error'] = stderr[:150] if stderr else 'Unknown error'

            except subprocess.TimeoutExpired:
                proc.kill()
                proc.communicate()
                result['load_time'] = self.timeout_seconds
                result['status'] = 'TIMEOUT'
                result['error'] = f'Timeout after {self.timeout_seconds}s'

        except Exception as e:
            result['load_time'] = time.time() - start_time
            result['status'] = 'FAILED'
            result['error'] = str(e)[:150]

        return result

    def find_ptrac_files(self):
        """Find all PTRAC-like files in the directory"""
        ptrac_files = []
        for pattern in ['**/*.ptrac', '**/*.h5', '**/*.ip', '**/*.p']:
            ptrac_files.extend(self.base_dir.glob(pattern))
        return sorted(ptrac_files)

    def run_tests(self):
        """Run tests on all PTRAC files"""
        print("=" * 100)
        print(f"PTRAC FILES TEST SUITE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 100)

        ptrac_files = self.find_ptrac_files()

        if not ptrac_files:
            print(f"\nNo PTRAC files found in {self.base_dir}")
            return

        print(f"\nFound {len(ptrac_files)} potential PTRAC files")
        print(f"Timeout per file: {self.timeout_seconds}s (HARD LIMIT)")
        print(f"Max histories: 2-5 depending on file size\n")

        # Test each file
        for i, filepath in enumerate(ptrac_files, 1):
            print(f"[{i}/{len(ptrac_files)}] Testing: {filepath.name:<50} ", end='', flush=True)

            result = self.test_file(filepath)
            self.results.append(result)

            # Print status
            if result['status'] == 'SUCCESS':
                print(f"[OK] {result['load_time']:.2f}s")
            elif result['status'] == 'PARTIAL':
                print(f"[!] PARTIAL")
            elif result['status'] == 'FAILED':
                print(f"[X] FAILED")
            elif result['status'] == 'TIMEOUT':
                print(f"[T] TIMEOUT")
            elif result['status'] == 'SKIPPED':
                print(f"[-] SKIP")

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print detailed summary of results"""
        print("\n" + "=" * 100)
        print("TEST RESULTS SUMMARY")
        print("=" * 100)

        # Count by status
        status_counts = {}
        for result in self.results:
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        print("\n[STATS] OVERALL:")
        print(f"  Total files: {len(self.results)}")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")

        # Success files
        success = [r for r in self.results if r['status'] == 'SUCCESS']
        if success:
            print(f"\n[OK] SUCCESSFUL ({len(success)} files):")
            for r in success:
                print(f"  {r['file']:<50} | {r['format']:<10} | {r['size']:<10} | "
                      f"{r['histories_count']} hist | {r['load_time']:.2f}s")

        # Timeout files
        timeout = [r for r in self.results if r['status'] == 'TIMEOUT']
        if timeout:
            print(f"\n[T] TIMEOUT ({len(timeout)} files):")
            for r in timeout:
                print(f"  {r['file']:<50} | {r['size']:<10} | Blocked > {self.timeout_seconds}s")

        # Failed files
        failed = [r for r in self.results if r['status'] == 'FAILED']
        if failed:
            print(f"\n[X] FAILED ({len(failed)} files):")
            for r in failed:
                print(f"  {r['file']:<50} | {r['format']:<10} | {r['size']:<10}")
                if r['error']:
                    print(f"      Error: {r['error']}")

        # Format statistics
        print("\n[FILE] BY FORMAT:")
        format_stats = {}
        for r in self.results:
            if r['status'] == 'SKIPPED':
                continue
            fmt = r['format']
            if fmt not in format_stats:
                format_stats[fmt] = {'total': 0, 'success': 0, 'failed': 0, 'timeout': 0}
            format_stats[fmt]['total'] += 1
            if r['status'] == 'SUCCESS':
                format_stats[fmt]['success'] += 1
            elif r['status'] == 'FAILED':
                format_stats[fmt]['failed'] += 1
            elif r['status'] == 'TIMEOUT':
                format_stats[fmt]['timeout'] += 1

        for fmt, stats in sorted(format_stats.items()):
            if stats['total'] > 0:
                print(f"  {fmt:<15} | Total: {stats['total']:2} | "
                      f"OK: {stats['success']:2} | Failed: {stats['failed']:2} | Timeout: {stats['timeout']:2}")

        # Size categories
        print("\n[SIZE] BY FILE SIZE:")
        size_categories = {'< 1MB': [], '1-10MB': [], '10-100MB': [], '> 100MB': []}
        for r in self.results:
            if r['status'] == 'SKIPPED':
                continue
            if r['size_mb'] < 1:
                size_categories['< 1MB'].append(r)
            elif r['size_mb'] < 10:
                size_categories['1-10MB'].append(r)
            elif r['size_mb'] < 100:
                size_categories['10-100MB'].append(r)
            else:
                size_categories['> 100MB'].append(r)

        for category, files in size_categories.items():
            if files:
                success_count = sum(1 for f in files if f['status'] == 'SUCCESS')
                print(f"  {category:<15} | {len(files):2} files | {success_count:2} OK")

        # Recommendations
        print("\n" + "=" * 100)
        print("\n[INFO] RECOMMENDATIONS:")

        binary_failed = [r for r in failed if 'BINARY' in r['format']]
        if binary_failed:
            print(f"  • {len(binary_failed)} BINARY files failed - binary format not supported")

        if timeout:
            print(f"  • {len(timeout)} files TIMEOUT - too slow or blocking (> {self.timeout_seconds}s)")
            print(f"    Consider avoiding these files in production")

        if success:
            print(f"  • {len(success)} files work perfectly - use these in DECIMA")

        # List reliable files
        reliable = [r for r in success if r['size_mb'] < 10 and r['load_time'] < 1]
        if reliable:
            print(f"\n[BEST] FAST & RELIABLE FILES ({len(reliable)} files, < 10MB, < 1s):")
            for r in sorted(reliable, key=lambda x: x['load_time']):
                print(f"  • {r['file']:<50} ({r['load_time']:.3f}s)")

        print("\n" + "=" * 100)


def main():
    """Main entry point"""
    tester = PTRACTester()
    tester.run_tests()


if __name__ == "__main__":
    main()
