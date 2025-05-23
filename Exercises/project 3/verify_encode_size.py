import os
import subprocess
import sys
import time

# --- Configuration ---
# Path to your Encode.py script. Assumes it's in the same directory.
ENCODE_PY_SCRIPT = "Encode.py"

# Timeout for each encoding process (in seconds)
ENCODE_TIMEOUT = 180 # Increased slightly for potentially larger files

# Test cases - assumes these input files exist in the script's directory
TEST_CASES = [
    {
        "name": "empty.txt",
        "original_size_bytes": 0,
        "expected_compressed_size_bytes": 1024
    },
    {
        "name": "oneByte.txt",
        "original_size_bytes": 1,
        "expected_compressed_size_bytes": 1025
    },
    {
        "name": "same.txt",
        "original_size_bytes": 100000,
        "expected_compressed_size_bytes": 13524
    },
    {
        "name": "KingJamesBible.txt",
        "original_size_bytes": 4948914,
        "expected_compressed_size_bytes": 2771852
    },
    {
        "name": "ScardoviaWiggsiae.dna",
        "original_size_bytes": 1576664,
        "expected_compressed_size_bytes": 446970
    },
    {
        "name": "DolphinSunset.jpg",
        "original_size_bytes": 416318,
        "expected_compressed_size_bytes": 416727
    },
]

# --- Helper Functions ---

def run_single_test(test_case_info):
    """Runs a single test case for Encode.py, assuming input file exists."""
    input_filename = test_case_info["name"]
    # Use a distinct name for compressed files
    compressed_filename = f"{os.path.splitext(input_filename)[0]}.encoded_output_test"
    expected_compressed_sz = test_case_info["expected_compressed_size_bytes"]
    expected_original_sz = test_case_info["original_size_bytes"]

    print(f"\n--- Testing '{input_filename}' ---")

    # 1. Verify input file exists
    if not os.path.exists(input_filename):
        print(f"  ERROR: Input file '{input_filename}' not found. Please ensure it's in the script's directory.")
        return "skipped", input_filename, compressed_filename # Indicate test was skipped

    # 2. Verify original file size (sanity check)
    actual_original_size = os.path.getsize(input_filename)
    if actual_original_size != expected_original_sz:
        print(f"  WARNING: Original size of '{input_filename}' is {actual_original_size} bytes, "
              f"but test case expected {expected_original_sz} bytes.")
        print(f"           Proceeding with the test using the actual file '{input_filename}'.")
        # This is a warning, not a fatal error for the test itself unless it implies a completely wrong file.

    # 3. Run Encode.py
    command = [sys.executable, ENCODE_PY_SCRIPT, input_filename, compressed_filename]
    print(f"  Running: {' '.join(command)}")

    if not os.path.exists(ENCODE_PY_SCRIPT):
        print(f"  FATAL ERROR: '{ENCODE_PY_SCRIPT}' not found. Please place it in the same directory as this script.")
        return "error", input_filename, compressed_filename # Critical script error

    start_time = time.time()
    try:
        # Using check=False to manually inspect returncode
        process = subprocess.run(command, capture_output=True, text=True, timeout=ENCODE_TIMEOUT, check=False)
        duration = time.time() - start_time
        print(f"  '{ENCODE_PY_SCRIPT}' completed in {duration:.2f} seconds.")

        if process.returncode != 0:
            print(f"  ERROR: '{ENCODE_PY_SCRIPT}' failed for '{input_filename}'.")
            print(f"  Return code: {process.returncode}")
            if process.stdout and process.stdout.strip():
                print(f"  Stdout:\n------\n{process.stdout.strip()}\n------")
            if process.stderr and process.stderr.strip():
                print(f"  Stderr:\n------\n{process.stderr.strip()}\n------")
            return "error", input_filename, compressed_filename # Encode.py reported an error

    except FileNotFoundError: # Should be caught by the ENCODE_PY_SCRIPT check, but for safety
        print(f"  ERROR: Python interpreter or '{ENCODE_PY_SCRIPT}' not found during subprocess call.")
        return "error", input_filename, compressed_filename
    except subprocess.TimeoutExpired:
        print(f"  ERROR: '{ENCODE_PY_SCRIPT}' timed out after {ENCODE_TIMEOUT} seconds for '{input_filename}'.")
        return "error", input_filename, compressed_filename
    except Exception as e:
        print(f"  An unexpected error occurred while running '{ENCODE_PY_SCRIPT}': {e}")
        return "error", input_filename, compressed_filename

    # 4. Check if compressed file was created and its size
    if not os.path.exists(compressed_filename):
        print(f"  ERROR: Compressed file '{compressed_filename}' was not created by '{ENCODE_PY_SCRIPT}'.")
        return "error", input_filename, compressed_filename # Encode.py didn't produce output

    actual_compressed_size = os.path.getsize(compressed_filename)
    print(f"  Expected compressed size: {expected_compressed_sz} bytes")
    print(f"  Actual compressed size:   {actual_compressed_size} bytes")

    # 5. Compare and report
    if actual_compressed_size == expected_compressed_sz:
        print(f"  RESULT: PASS for '{input_filename}'")
        return "pass", input_filename, compressed_filename
    else:
        diff = actual_compressed_size - expected_compressed_sz
        print(f"  RESULT: FAIL for '{input_filename}' (Difference: {diff} bytes)")
        return "fail", input_filename, compressed_filename

# --- Main Execution ---

def main():
    print("Starting verification of Encode.py output sizes (input files must exist)...")
    print("===========================================================================")
    print(f"Please ensure '{ENCODE_PY_SCRIPT}' and all 6 test input files are in the same directory as this script:")
    for tc in TEST_CASES:
        print(f"  - {tc['name']}")
    print("===========================================================================")


    results_summary = {"pass": 0, "fail": 0, "error": 0, "skipped": 0}
    # Store dicts of {"status": status, "input": input_file, "compressed": compressed_file}
    generated_files_details = []

    for case_info in TEST_CASES:
        status, input_f, compressed_f = run_single_test(case_info)
        results_summary[status] += 1
        # Store details for cleanup, regardless of status, if compressed_f was defined
        if compressed_f:
             generated_files_details.append({"input": input_f, "compressed": compressed_f})


    print("\n\n--- Verification Summary ---")
    print(f"Total tests defined: {len(TEST_CASES)}")
    print(f"  Passed:  {results_summary['pass']}")
    print(f"  Failed:  {results_summary['fail']}")
    print(f"  Errors:  {results_summary['error']} (Encode.py crashed, script issue, or output not created)")
    print(f"  Skipped: {results_summary['skipped']} (Input file missing)")
    print("===========================================================================")

    if results_summary["fail"] == 0 and results_summary["error"] == 0 and results_summary["skipped"] == 0:
        print("All tests passed successfully!")
    elif results_summary["fail"] == 0 and results_summary["error"] == 0 and results_summary["skipped"] > 0:
        print("All runnable tests passed. Some were skipped due to missing input files.")
    else:
        print("Some tests did not pass. Please review the output above.")

    # Cleanup: Only remove generated compressed files
    print("\n--- Cleaning up generated compressed files ---")
    cleaned_count = 0
    for detail in generated_files_details:
        compressed_file_to_remove = detail["compressed"]
        if os.path.exists(compressed_file_to_remove):
            try:
                os.remove(compressed_file_to_remove)
                print(f"  Removed compressed file: {compressed_file_to_remove}")
                cleaned_count +=1
            except OSError as e:
                print(f"  Error removing compressed file {compressed_file_to_remove}: {e}")
    if not generated_files_details:
        print("  No compressed files were marked for cleanup.")
    elif cleaned_count == 0 and any(os.path.exists(d["compressed"]) for d in generated_files_details):
        print("  Some compressed files may still exist if they were not properly tracked or errors occurred before tracking.")
    print("Cleanup complete.")


if __name__ == "__main__":
    main()