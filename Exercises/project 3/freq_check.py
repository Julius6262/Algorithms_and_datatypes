def count_frequencies(filename):
    freq = [0] * 256
    with open(filename, "rb") as f:
        while True:
            b = f.read(1)
            if not b:
                break
            freq[b[0]] += 1
    return freq

if __name__ == "__main__":
    filename = "ScardoviaWiggsiae.dna"
    freqs = count_frequencies(filename)
    print(f"Frequency analysis for {filename}:")
    print("Total bytes:", sum(freqs))
    print("Non-zero frequencies:", sum(1 for x in freqs if x > 0))
    print("Top 10 frequencies:")
    top10 = sorted([(i, x) for i, x in enumerate(freqs)], key=lambda x: x[1], reverse=True)[:10]
    for byte, count in top10:
        print(f"Byte {byte} (0x{byte:02X}): {count}")
