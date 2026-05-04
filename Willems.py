# willems_fast.py

_fingerprint_cache = {}

def pack_fingerprint(fp):
    """
    Convert a binary string fingerprint into a list of 64-bit integers.
    Uses caching for speed.
    """
    if fp in _fingerprint_cache:
        return _fingerprint_cache[fp]

    packed = []
    for i in range(0, len(fp), 64):
        chunk = fp[i:i+64]
        if len(chunk) < 64:
            chunk = chunk.ljust(64, "0")
        packed.append(int(chunk, 2))

    _fingerprint_cache[fp] = packed
    return packed


def willems(fp1, fp2, weights=None):
    A = pack_fingerprint(fp1)
    B = pack_fingerprint(fp2)

    numerator = 0.0
    denominator = 0.0
    base_index = 0

    for a, b in zip(A, B):
        union = a | b
        intersection = a & b

        while union:
            bit = union & -union
            local_pos = bit.bit_length() - 1
            idx = base_index + (63 - local_pos)

            # default weight = 1
            w = weights.get(idx, 1) if weights else 1

            # apply weight to BOTH numerator and denominator
            denominator += w

            if intersection & bit:
                numerator += w

            union ^= bit

        base_index += 64

    return numerator / denominator if denominator else 0