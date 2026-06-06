# Algoritmo Insertion Sort
def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

# Algoritmo Merge Sort
def merge_sort(arr):
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
            k += 1
        while i < len(L):
            a[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            a[k] = R[j]
            j += 1
            k += 1

    def _sort(a, lo, hi):
        if lo < hi:
            mid = (lo + hi) // 2
            _sort(a, lo, mid)
            _sort(a, mid + 1, hi)
            _merge(a, lo, mid, hi)

    a = arr[:]
    _sort(a, 0, len(a) - 1)
    return a
