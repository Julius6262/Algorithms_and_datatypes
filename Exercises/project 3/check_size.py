import os
import subprocess

def test_encoding_size(input_file, expected_size):
    compressed_file = input_file.replace(".txt", ".bin")

    # Run Encode.py
    result = subprocess.run(["python", "Encode.py", input_file, compressed_file], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Encode failed for {input_file}: {result.stderr}")
        return

    # Get actual file size
    actual_size = os.path.getsize(compressed_file)

    # Compare with expected
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
