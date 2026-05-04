import random
import csv


# -----------------------------
# Generate fingerprint
# -----------------------------
def generate_fingerprint(length=128, sparsity=0.1):
    return [1 if random.random() < sparsity else 0 for _ in range(length)]


# -----------------------------
# Generate fake SMILES string
# -----------------------------
def generate_smiles():
    chars = "CNOPSH123456()="
    return "".join(random.choice(chars) for _ in range(random.randint(10, 25)))


# -----------------------------
# Create dataset
# -----------------------------
def generate_dataset(n=100, fp_length=128):
    data = []

    for i in range(n):
        mol = {
            "CID": f"mol_{i}",  # ✅ consistent ID name used everywhere
            "smiles": generate_smiles(),
            "fingerprint": generate_fingerprint(fp_length)
        }
        data.append(mol)

    return data


# -----------------------------
# Save dataset to CSV
# -----------------------------
def save_to_csv(data, filename="sample_data.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # header (must match all benchmark scripts)
        writer.writerow(["CID", "smiles", "fingerprint"])

        for row in data:
            writer.writerow([
                row["CID"],
                row["smiles"],
                "".join(map(str, row["fingerprint"]))
            ])


# -----------------------------
# Run script
# -----------------------------
if __name__ == "__main__":
    data = generate_dataset(n=100, fp_length=128)
    save_to_csv(data)
    print("Sample dataset generated: sample_data.csv")