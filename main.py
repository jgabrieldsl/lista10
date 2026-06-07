import csv
import math
import os
import random
import time

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
            a[k] = L[i] if L[i] <= R[j] else R[j]
            i, j = (i + 1, j) if L[i] <= R[j] else (i, j + 1)
            counter[0] += 1
            k += 1
        for v in L[i:]:
            a[k] = v; k += 1; counter[0] += 1
        for v in R[j:]:
            a[k] = v; k += 1; counter[0] += 1

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

# Configurações do benchmark
ALGORITHMS = {
    "Insertion Sort": insertion_sort,
    "Merge Sort":     merge_sort,
    "Quick Sort":     quick_sort,
}
SIZES   = [1_000, 10_000, 100_000]
RUNS    = 3
TIMEOUT = 300

def generate_vector(size, seed=42):
    rng = random.Random(seed)
    return [rng.randint(1, size * 10) for _ in range(size)]

def run_benchmarks():
    results = {}
    for size in SIZES:
        original = generate_vector(size)
        for name, fn in ALGORITHMS.items():
            times, ops, timed_out = [], [], False
            for run in range(1, RUNS + 1):
                t0 = time.perf_counter()
                _, moves = fn(original[:])
                elapsed = time.perf_counter() - t0
                if elapsed > TIMEOUT:
                    timed_out = True
                    break
                times.append(elapsed)
                ops.append(moves)
            if timed_out:
                results[(name, size)] = {"times": times, "ops": ops, "timed_out": True}
            else:
                avg = sum(times) / len(times)
                std = math.sqrt(sum((t - avg) ** 2 for t in times) / len(times))
                avg_ops = sum(ops) / len(ops)
                results[(name, size)] = {
                    "times": times, "ops": ops,
                    "avg": avg, "std": std, "avg_ops": avg_ops,
                    "timed_out": False,
                }
    return results

def export_csv(results, path):
    header = ["Algoritmo", "Tamanho",
              "Tempo 1 (s)", "Tempo 2 (s)", "Tempo 3 (s)",
              "Tempo Médio (s)", "Desvio Padrão (s)",
              "Trocas/Movimentações Médias", "Timeout?"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for name in ALGORITHMS:
            for size in SIZES:
                r = results[(name, size)]
                t = r["times"]
                w.writerow([
                    name, size,
                    f"{t[0]:.6f}" if len(t) > 0 else "N/A",
                    f"{t[1]:.6f}" if len(t) > 1 else "N/A",
                    f"{t[2]:.6f}" if len(t) > 2 else "N/A",
                    f"{r['avg']:.6f}"    if not r["timed_out"] else "N/A",
                    f"{r['std']:.6f}"    if not r["timed_out"] else "N/A",
                    f"{r['avg_ops']:.0f}" if not r["timed_out"] else "N/A",
                    "Sim" if r["timed_out"] else "Não",
                ])

if __name__ == "__main__":
    results = run_benchmarks()
    export_csv(results, "resultados_benchmark.csv")
