import random

# Algoritmo Insertion Sort
def insertion_sort(arr):
    a = arr[:]
    moves = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            moves += 1
            j -= 1
        a[j + 1] = key
        if j + 1 != i:
            moves += 1
    return a, moves

# Algoritmo Merge Sort
def merge_sort(arr):
    counter = [0]

    def _merge(a, left, mid, right):
        L = a[left : mid + 1]
        R = a[mid + 1 : right + 1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            counter[0] += 1
            k += 1
        while i < len(L):
            a[k] = L[i]
            i += 1
            k += 1
            counter[0] += 1
        while j < len(R):
            a[k] = R[j]
            j += 1
            k += 1
            counter[0] += 1

    def _sort(a, lo, hi):
        if lo < hi:
            mid = (lo + hi) // 2
            _sort(a, lo, mid)
            _sort(a, mid + 1, hi)
            _merge(a, lo, mid, hi)

    a = arr[:]
    _sort(a, 0, len(a) - 1)
    return a, counter[0]

# Algoritmo Quick Sort
def quick_sort(arr):
    counter = [0]

    def _partition(a, lo, hi):
        pivot_idx = random.randint(lo, hi)
        a[pivot_idx], a[hi] = a[hi], a[pivot_idx]
        counter[0] += 1
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            if a[j] <= pivot:
                i += 1
                if i != j:
                    a[i], a[j] = a[j], a[i]
                    counter[0] += 1
        a[i + 1], a[hi] = a[hi], a[i + 1]
        counter[0] += 1
        return i + 1

    a = arr[:]
    if len(a) > 1:
        stack = [(0, len(a) - 1)]
        while stack:
            lo, hi = stack.pop()
            if lo < hi:
                p = _partition(a, lo, hi)
                stack.append((lo, p - 1))
                stack.append((p + 1, hi))
    return a, counter[0]
