import csv
from rdkit import Chem
from rdkit.Chem import AllChem

input_file = "data/Compound_002500001_003000000.sdf"
output_file = "data/pubchem_fingerprints_File3.csv"

suppl = Chem.SDMolSupplier(input_file)

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["CID", "fingerprint"])

    count = 0

    for mol in suppl:
        if mol is None:
            continue

        try:
            cid = mol.GetProp("PUBCHEM_COMPOUND_CID")

            # Generate 881-bit fingerprint
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=881)
            bitstring = fp.ToBitString()

            writer.writerow([cid, bitstring])
            count += 1

            if count % 10000 == 0:
                print("Processed", count)

        except:
            continue

print("Finished:", count, "molecules")