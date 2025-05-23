import os
import subprocess

def get_compressed_filename(input_file):
    base, _ = os.path.splitext(input_file)
    return base + ".bin"

def test_encoding_size(input_file, expected_size):
    compressed_file = get_compressed_filename(input_file)

    # Run Encode.py on input_file, output to compressed_file
    result = subprocess.run(
        ["python", "Encode.py", input_file, compressed_file],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Encode failed for {input_file}: {result.stderr.strip()}")
        return

    if not os.path.exists(compressed_file):
        print(f"❌ Encode output file {compressed_file} not found for {input_file}")
        return

    actual_size = os.path.getsize(compressed_file)

    print(f"\n📦 {input_file}:")
    print(f"   Expected size → {expected_size} bytes")
    print(f"   Actual size   → {actual_size} bytes")

    if actual_size == expected_size:
        print("   ✅ PASS: Size matches")
    else:
        print("   ❌ FAIL: Size does not match")

def run_size_tests():
    print("\n==============================")
    print("🧪 Checking Encoded File Sizes")
    print("==============================")

    test_cases = [
        ("KingJamesBible.txt", 2771852),
        ("ScardoviaWiggsiae.dna", 446970),
        ("DolphinSunset.jpg", 416727),
        ("same.txt", 13524),
        ("oneByte.txt", 1025),
        ("empty.txt", 1024),
    ]

    for filename, expected_size in test_cases:
        if not os.path.exists(filename):
            print(f"⚠️ Skipping {filename}: File not found.")
            continue
        test_encoding_size(filename, expected_size)

if __name__ == "__main__":
    run_size_tests()
