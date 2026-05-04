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

def main():

    print("Loading dataset...")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # IMPORTANT: use the equal bucket dataset
    DATA_PATH = os.path.join(BASE_DIR, "data", "pubchem_equal_buckets.csv")

    df = pd.read_csv(
    DATA_PATH,
    usecols=["fingerprint", "bucket_equal"],  # include the bucket column
    dtype={"fingerprint": str, "bucket_equal": int},  # ensure correct type
)

    print("Total molecules:", len(df))
    print(df.head())

    query_fp = df.iloc[0]["fingerprint"]
    threshold = 0.75
    weights = {24:5} 
    

    # -----------------------------
    # BRUTE FORCE
    # -----------------------------
    print("\nRunning brute force search...")

    start = time.time()
    brute_results = brute_force_search(query_fp, df["fingerprint"], threshold)
    brute_force_time = time.time() - start

    print("Brute force results:", len(brute_results))
    print("Brute force time:", brute_force_time, "seconds")

    print("\nTop 5 most similar (Brute Force):")

    brute_scored = []

    for fp in df["fingerprint"]:
        sim = tanimoto(query_fp, fp)
        brute_scored.append((fp, sim))

    brute_scored.sort(key=lambda x: x[1], reverse=True)

    for fp, sim in brute_scored[:20]:
        print(sim)


    # -----------------------------
    # BITCOUNT BUCKETS
    # -----------------------------
    print("\nBuilding bitcount buckets...")

    start_bucket_build = time.time()
    buckets = build_buckets(df["fingerprint"])
    bucket_build_time = time.time() - start_bucket_build

    print("Total bitcount buckets:", len(buckets))

    print("\nRunning bitcount bucket search...")

    start = time.time()
    bucket_results, checked = bucket_search(query_fp, buckets, threshold)
    bucket_search_time = time.time() - start

    print("Bucket search results:", len(bucket_results))
    print("Bucket search time:", bucket_search_time, "seconds")
    print("Fingerprints checked:", checked)

    print("\nTop 5 most similar (Bitcount Buckets):")

    bucket_scored = []

    for fp in bucket_results:
        sim = tanimoto(query_fp, fp)
        bucket_scored.append((fp, sim))

    bucket_scored.sort(key=lambda x: x[1], reverse=True)

    for fp, sim in bucket_scored[:20]:
        print(sim)


    # -----------------------------
    # EQUAL BUCKETS
    # -----------------------------
    print("\nBuilding equal-frequency buckets...")

    start_equal_build = time.time()

    equal_buckets = {}

    for fp, bucket in zip(df["fingerprint"], df["bucket_equal"]):

        bucket = int(bucket)

        if bucket not in equal_buckets:
            equal_buckets[bucket] = []

        equal_buckets[bucket].append(fp)

    equal_build_time = time.time() - start_equal_build

    print("Total equal buckets:", len(equal_buckets))


    print("\nRunning equal bucket search...")

    start = time.time()

    equal_results = []
    equal_checked = 0

    query_bucket = int(df.iloc[0]["bucket_equal"])

    # search query bucket and neighbors
    for b in [query_bucket - 1, query_bucket, query_bucket + 1]:

        if b in equal_buckets:

            for fp in equal_buckets[b]:

                equal_checked += 1

                sim = tanimoto(query_fp, fp)

                if sim >= threshold:
                    equal_results.append(fp)

    equal_search_time = time.time() - start

    print("Equal bucket results:", len(equal_results))
    print("Equal bucket time:", equal_search_time, "seconds")
    print("Fingerprints checked:", equal_checked)


    # -----------------------------
    # SPEED COMPARISON
    # -----------------------------
    print("\nSpeed comparison")

    speedup_bitcount = brute_force_time / bucket_search_time
    speedup_equal = brute_force_time / equal_search_time

    print("Bitcount speedup:", speedup_bitcount)
    print("Equal bucket speedup:", speedup_equal)

    print("\nTop 5 most similar (Equal Buckets):")

    equal_scored = []

    for fp in equal_results:
        sim = tanimoto(query_fp, fp)
        equal_scored.append((fp, sim))

    equal_scored.sort(key=lambda x: x[1], reverse=True)

    for fp, sim in equal_scored[:20]:
        print(sim)


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

    equal_build_time,
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

                "equal_build_time",
                "equal_search_time",
                "equal_checked",
                "equal_speedup"
            ])

        writer.writerow(row)


if __name__ == "__main__":
    main()