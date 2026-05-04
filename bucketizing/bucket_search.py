import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tanimoto import tanimoto
from Willems import willems

def bucket_search(query_fp, buckets, threshold=0.75):

    results = []
    checked = 0
    weights = {24:5} 

    # query bitcount
    a = query_fp.count("1")

    # valid range
    b_min = math.ceil(threshold * a)
    b_max = math.floor(a / threshold)

    # loop over bucket ranges
    for (low, high), candidates in buckets.items():

        # check if bucket overlaps valid range
        if high < b_min or low > b_max:
            continue  # skip bucket

        for fp in candidates:
            checked += 1

            similarity = tanimoto(query_fp, fp)

            if similarity >= threshold:
                results.append(fp)

    return results, checked