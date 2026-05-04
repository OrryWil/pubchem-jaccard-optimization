import time
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Willems import willems


def build_buckets(fingerprints, bucket_size):
    buckets = {}

    for fp in fingerprints:
        bc = fp.count("1")

        bucket_start = (bc // bucket_size) * bucket_size
        key = (bucket_start, bucket_start + bucket_size - 1)

        if key not in buckets:
            buckets[key] = []

        buckets[key].append(fp)

    return buckets


def get_valid_buckets(query_bc, threshold, buckets):
    lower = int(threshold * query_bc)
    upper = int(query_bc / threshold)

    valid = []

    for (low, high) in buckets.keys():
        if high >= lower and low <= upper:
            valid.append((low, high))

    return valid


def bucket_search(query_fp, buckets, threshold):
    query_bc = query_fp.count("1")

    valid_keys = get_valid_buckets(query_bc, threshold, buckets)

    candidates = []
    for key in valid_keys:
        candidates.extend(buckets[key])

    results = []

    for fp in candidates:
        sim = willems(query_fp, fp)
        if sim >= threshold:
            results.append(fp)

    return results, len(candidates)


def brute_force(query_fp, fingerprints, threshold):
    results = []

    for fp in fingerprints:
        sim = willems(query_fp, fp)
        if sim >= threshold:
            results.append(fp)

    return results


def main():

    DATA_PATH = "data/sample_data.csv"

    df = pd.read_csv(
        DATA_PATH,
        usecols=["fingerprint"],
        dtype={"fingerprint": str}
    )

    fingerprints = df["fingerprint"].tolist()

    query_fp = fingerprints[0]
    threshold = 0.75

    print("Running brute force baseline...")
    start = time.time()
    brute_results = brute_force(query_fp, fingerprints, threshold)
    brute_time = time.time() - start

    print(f"Brute force time: {brute_time:.2f}s")
    print(f"Brute results: {len(brute_results)}")

    bucket_sizes = [1, 2, 3, 5, 10, 20]

    print("\n--- Bucket Size Experiment ---\n")

    for size in bucket_sizes:

        print(f"\nBucket size: {size}")

        start = time.time()
        buckets = build_buckets(fingerprints, size)
        build_time = time.time() - start

        start = time.time()
        results, candidates_checked = bucket_search(
            query_fp, buckets, threshold
        )
        search_time = time.time() - start

        # accuracy (overlap with brute force)
        overlap = len(set(results) & set(brute_results))
        accuracy = overlap / len(brute_results) if brute_results else 0

        print(f"Build time: {build_time:.2f}s")
        print(f"Search time: {search_time:.2f}s")
        print(f"Candidates checked: {candidates_checked}")
        print(f"Results found: {len(results)}")
        print(f"Accuracy vs brute: {accuracy:.4f}")


if __name__ == "__main__":
    main()