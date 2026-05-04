import pandas as pd
import os
import time
import sys

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tanimoto import tanimoto
from Willems import willems

# Load fingerprints and CID
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "pubchem_800K.csv")

df = pd.read_csv(
    DATA_PATH,
    usecols=["CID", "fingerprint"],  # include CID for easier identification
    dtype={"CID": str, "fingerprint": str}
)

query_fp = df.iloc[0]["fingerprint"]
query_cid = df.iloc[0]["CID"]

# Example user weights for Willems similarity
weights = {} #{24:5} 

# -----------------------------
# Run Tanimoto benchmark
# -----------------------------
start = time.time()
tanimoto_scores = [(row.CID, row.fingerprint, tanimoto(query_fp, row.fingerprint)) for row in df.itertuples()]
tanimoto_time = time.time() - start

# Sort by similarity descending
tanimoto_scores.sort(key=lambda x: x[2], reverse=True)

# -----------------------------
# Run Willems benchmark
# -----------------------------
print(weights)
start = time.time()
willems_scores = [(row.CID, row.fingerprint, willems(query_fp, row.fingerprint, weights)) for row in df.itertuples()]
willems_time = time.time() - start

# Sort by similarity descending
willems_scores.sort(key=lambda x: x[2], reverse=True)

# -----------------------------
# Print results
# -----------------------------
print("Tanimoto time:", tanimoto_time)
print("Willems time:", willems_time)

# -----------------------------
# Print top n with CID and fingerprints
# -----------------------------
topn = 20
print("\nTop 5 molecules by Tanimoto similarity:")
for cid, fp, sim in tanimoto_scores[:topn]:
    print(f"CID: {cid}, Similarity: {sim}")

print("\nTop 5 molecules by Willems similarity:")
for cid, fp, sim in willems_scores[:topn]:
    print(f"CID: {cid}, Similarity: {sim}")



