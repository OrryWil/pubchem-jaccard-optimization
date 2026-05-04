import pandas as pd

df1 = pd.read_csv("data/pubchem_fingerprints.csv", dtype=str)
df2 = pd.read_csv("data/pubchem_fingerprints_File2.csv", dtype=str)
df3 = pd.read_csv("data/pubchem_fingerprints_File3.csv", dtype=str)

combined = pd.concat([df1, df2, df3])

combined.to_csv("data/pubchem_1350K.csv", index=False)

print("Total molecules:", len(combined))