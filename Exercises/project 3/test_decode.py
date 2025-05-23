import sys
# ------------------------------------------
# ✅ TEST SECTION (can go at end of Decode.py)
# ------------------------------------------
import subprocess

def run_test_case(content_bytes, label):
    input_file = f"{label}_input.bin"
    encoded_file = f"{label}_encoded.bin"
    decoded_file = f"{label}_decoded.bin"

    # Write input content
    with open(input_file, "wb") as f:
        f.write(content_bytes)
    print(f"\n🔹 Test: {label}")
    print(f"  Input size: {len(content_bytes)} bytes")

    # Encode
    result_enc = subprocess.run(["python", "Encode.py", input_file, encoded_file], capture_output=True, text=True)
    if result_enc.returncode != 0:
        print(f"❌ Encode.py failed: {result_enc.stderr}")
        return

    # Decode
    result_dec = subprocess.run(["python", "Decode.py", encoded_file, decoded_file], capture_output=True, text=True)
    if result_dec.returncode != 0:
        print(f"❌ Decode.py failed: {result_dec.stderr}")
        return

    # Compare input and output
    with open(input_file, "rb") as fin, open(decoded_file, "rb") as fout:
        original = fin.read()
        decoded = fout.read()

    if original == decoded:
        print(f"✅ PASS: Output matches original for '{label}'")
    else:
        print(f"❌ FAIL: Output does NOT match for '{label}'")

    # Clean up
    for file in [input_file, encoded_file, decoded_file]:
        try:
            os.remove(file)
        except:
            pass

def run_decode_tests():
    print("\n==========================")
    print("🧪 Testing Decode.py")
    print("==========================")

    # Test 1: Simple ASCII string
    run_test_case(b"aabbccc", "simple")

    # Test 2: All byte values once (0–255)
    run_test_case(bytes(range(256)), "all_bytes")

    # Test 3: Long random sequence
    run_test_case(b"the quick brown fox jumps over the lazy dog" * 10, "long_text")

if __name__ == "__main__" and "decode" in sys.argv[0].lower():
    run_decode_tests()
