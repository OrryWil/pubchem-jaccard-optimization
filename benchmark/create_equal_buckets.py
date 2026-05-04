import pandas as pd
import numpy as np

INPUT_FILE = "data/pubchem_fingerprints.csv"
OUTPUT_FILE = "data/pubchem_equal_bucketsSmall.csv"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE, dtype=str)

print("Total molecules:", len(df))

# compute bitcounts
bitcounts = [fp.count("1") for fp in df["fingerprint"]]

num_buckets = 10

print("Computing bucket boundaries...")

boundaries = np.quantile(bitcounts, np.linspace(0, 1, num_buckets + 1))

buckets_equal = {i: [] for i in range(num_buckets)}
bucket_assignments = []

print("Assigning fingerprints to buckets...")

for fp, bc in zip(df["fingerprint"], bitcounts):

    for i in range(num_buckets):

        if boundaries[i] <= bc <= boundaries[i + 1]:

            buckets_equal[i].append(fp)
            bucket_assignments.append(i)
            break


df_equal = df.copy()
df_equal["bucket_equal"] = bucket_assignments

print("Saving new dataset...")

df_equal.to_csv(OUTPUT_FILE, index=False)

print("Equal-frequency bucket file saved.")