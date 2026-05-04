import os
import sys
import time
import csv
import pandas as pd

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from brute_force.brute_force import brute_force_search
from bucketizing.build_buckets import build_buckets
from bucketizing.bucket_search import bucket_search
from tanimoto import tanimoto
from Willems import willems


def assign_equal_buckets(fingerprints, num_buckets=10):
    """
    Dynamically assign equal-frequency buckets.
    Replaces missing bucket_equal column.
    """
    buckets = {}
    for i, fp in enumerate(fingerprints):
        bucket_id = i % num_buckets
        if bucket_id not in buckets:
            buckets[bucket_id] = []
        buckets[bucket_id].append(fp)

    return buckets, [i % num_buckets for i in range(len(fingerprints))]


def main():

    print("Loading dataset...")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "sample_data.csv")

    df = pd.read_csv(
    DATA_PATH,
    usecols=["fingerprint"],
    dtype={"fingerprint": str}
)

    print("Total molecules:", len(df))
    print(df.head())

    query_fp = df.iloc[0]["fingerprint"]
    threshold = 0.75

    # Optional weights (your Willems method)
    weights = {24: 5}

    # -----------------------------
    # BRUTE FORCE
    # -----------------------------
    print("\nRunning brute force search...")

    start = time.time()
    brute_results = brute_force_search(query_fp, df["fingerprint"], threshold)
    brute_force_time = time.time() - start

    print("Brute force results:", len(brute_results))
    print("Brute force time:", brute_force_time, "seconds")

    # -----------------------------
    # FULL SCORING (DEBUG / TOP RESULTS)
    # -----------------------------
    brute_scored = []
    for fp in df["fingerprint"]:
        sim = tanimoto(query_fp, fp)
        brute_scored.append((fp, sim))

    brute_scored.sort(key=lambda x: x[1], reverse=True)

    print("\nTop 5 (Brute Force):")
    for fp, sim in brute_scored[:5]:
        print(sim)

    # -----------------------------
    # BITCOUNT BUCKETS
    # -----------------------------
    print("\nBuilding bitcount buckets...")

    start = time.time()
    buckets = build_buckets(df["fingerprint"])
    bucket_build_time = time.time() - start

    print("Total buckets:", len(buckets))

    print("\nRunning bucket search...")

    start = time.time()
    bucket_results, checked = bucket_search(query_fp, buckets, threshold)
    bucket_search_time = time.time() - start

    print("Bucket results:", len(bucket_results))
    print("Time:", bucket_search_time)
    print("Checked:", checked)

    # -----------------------------
    # EQUAL BUCKETS (FIXED - NO DATA DEPENDENCY)
    # -----------------------------
    print("\nBuilding equal-frequency buckets dynamically...")

    equal_buckets, bucket_labels = assign_equal_buckets(df["fingerprint"])

    print("Total equal buckets:", len(equal_buckets))

    query_bucket = bucket_labels[0]

    start = time.time()
    equal_results = []
    equal_checked = 0

    for b in [query_bucket - 1, query_bucket, query_bucket + 1]:
        if b in equal_buckets:
            for fp in equal_buckets[b]:
                equal_checked += 1
                sim = tanimoto(query_fp, fp)
                if sim >= threshold:
                    equal_results.append(fp)

    equal_search_time = time.time() - start

    print("Equal bucket results:", len(equal_results))
    print("Equal time:", equal_search_time)
    print("Checked:", equal_checked)

    # -----------------------------
    # SPEEDUP COMPARISON
    # -----------------------------
    print("\nSpeed comparison:")

    speedup_bitcount = brute_force_time / bucket_search_time
    speedup_equal = brute_force_time / equal_search_time

    print("Bitcount speedup:", speedup_bitcount)
    print("Equal bucket speedup:", speedup_equal)

    # -----------------------------
    # SAVE RESULTS
    # -----------------------------
    results_file = "benchmark_results.csv"

    row = [
        len(df),
        threshold,

        len(brute_results),
        len(bucket_results),
        len(equal_results),

        brute_force_time,
        bucket_build_time,
        bucket_search_time,
        checked,
        speedup_bitcount,

        equal_search_time,
        equal_checked,
        speedup_equal
    ]

    file_exists = os.path.isfile(results_file)

    with open(results_file, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "dataset_size",
                "threshold",
                "brute_results",
                "bitcount_results",
                "equal_results",
                "brute_force_time",
                "bitcount_build_time",
                "bitcount_search_time",
                "bitcount_checked",
                "bitcount_speedup",
                "equal_search_time",
                "equal_checked",
                "equal_speedup"
            ])

        writer.writerow(row)


if __name__ == "__main__":
    main()