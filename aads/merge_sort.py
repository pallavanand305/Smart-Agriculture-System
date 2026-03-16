"""
AADS Module — Merge Sort
Sorts sensor reading logs by timestamp for trend analysis.
Stable sort — O(n log n) time, O(n) space.
"""


def merge_sort(arr: list, key=lambda x: x) -> list:
    if len(arr) <= 1:
        return arr
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid],  key)
    right = merge_sort(arr[mid:],  key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ── Quick demo ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import random, time
    base = int(time.time())
    logs = [{"timestamp": base + random.randint(0, 3600), "moisture": random.randint(20, 80)}
            for _ in range(8)]
    sorted_logs = merge_sort(logs, key=lambda x: x["timestamp"])
    print("Sorted sensor logs by timestamp:")
    for log in sorted_logs:
        print(f"  t={log['timestamp']}  moisture={log['moisture']}%")
