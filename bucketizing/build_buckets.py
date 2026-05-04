def build_buckets(dataset, bucket_size=1):
    """
    Build buckets based on fingerprint bit count.

    bucket_size = 1 → exact buckets (original behavior)
    bucket_size > 1 → grouped buckets
    """
    buckets = {}

    for fp in dataset:
        bitcount = fp.count("1")

        # NEW: map into bucket range
        bucket_start = (bitcount // bucket_size) * bucket_size
        key = (bucket_start, bucket_start + bucket_size - 1)

        if key not in buckets:
            buckets[key] = []

        buckets[key].append(fp)

    return buckets