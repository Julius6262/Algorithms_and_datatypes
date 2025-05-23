import os
import subprocess

# List of files and expected sizes after encoding
files = [
    ("KingJamesBible.txt", 2771852),
    ("ScardoviaWiggsiae.dna", 446970),
    ("DolphinSunset.jpg", 416727),
    ("same.txt", 13524),
    ("oneByte.txt", 1025),
    ("empty.txt", 1024),
]

ENCODE_SCRIPT = "Encode.py"

def run_encode(input_file, output_file):
    result = subprocess.run([
        "python", ENCODE_SCRIPT, input_file, output_file
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error encoding {input_file}: {result.stderr}")
    return result.returncode == 0

def check_encoded_sizes():
    print(f"{'File':<25} {'Expected Size':>15} {'Actual Size':>15} {'Status':>10}")
    print("-" * 70)
    for input_file, expected_size in files:
        output_file = f"{input_file}.huff"
        success = run_encode(input_file, output_file)
        if success:
            actual_size = os.path.getsize(output_file)
            status = "OK" if actual_size == expected_size else "Mismatch"
            print(f"{input_file:<25} {expected_size:>15} {actual_size:>15} {status:>10}")
        else:
            print(f"{input_file:<25} {'-':>15} {'-':>15} {'Failed':>10}")

if __name__ == '__main__':
    check_encoded_sizes()