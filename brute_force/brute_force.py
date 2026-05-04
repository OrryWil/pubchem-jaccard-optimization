# brute_force.py
from tanimoto import tanimoto
from Willems import willems

def brute_force_search(query_fp, dataset, threshold=0.75):
    """
    dataset: a list or pandas Series of fingerprints (strings)
    """
    results = []
    weights =  {24:5} 

    for fp in dataset:  # just iterate directly
        similarity = willems(query_fp, fp, weights)
        if similarity >= threshold:
            results.append(fp)

    return results