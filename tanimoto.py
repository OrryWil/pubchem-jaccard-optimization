# Cache for packed fingerprints and popcounts
_fp_cache = {}

def pack_fingerprint(fp):
    """Convert binary string to integer (cached)."""
    if fp not in _fp_cache:
        packed = int(fp, 2)
        _fp_cache[fp] = (packed, packed.bit_count())
    return _fp_cache[fp]


def tanimoto(fp1, fp2):
    # Get packed fingerprints and precomputed bit counts
    p1, a = pack_fingerprint(fp1)
    p2, b = pack_fingerprint(fp2)

    # Intersection count using fast bitwise AND
    c = (p1 & p2).bit_count()

    denom = a + b - c
    if denom == 0:
        return 0

    return c / denom