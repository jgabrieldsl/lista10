import csv
import math
import os
import random
import time

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

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

PALETTE = {
    "Insertion Sort": "#E84393",
    "Merge Sort":     "#26A65B",
    "Quick Sort":     "#2980B9",
}

def _dark_ax(fig, ax):
    fig.patch.set_facecolor("#0D0D1A")
    ax.set_facecolor("#0D0D1A")
    ax.tick_params(colors="#AAAAAA")
    ax.spines[:].set_color("#333355")
    ax.grid(True, linestyle="--", alpha=0.3, color="#AAAAAA")

def _legend(ax):
    ax.legend(facecolor="#1A1A2E", edgecolor="#444466",
              labelcolor="white", fontsize=10)

def make_graphs(results, out_dir):
    if not HAS_MATPLOTLIB:
        return
    os.makedirs(out_dir, exist_ok=True)
    fmt_n  = ticker.FuncFormatter(lambda x, _: f"{int(x):,}")

    # 1. Linha: Tempo Médio (escala log) com tema escuro
    fig, ax = plt.subplots(figsize=(10, 6))
    _dark_ax(fig, ax)
    for algo, color in PALETTE.items():
        xs = SIZES
        ys = [results[(algo, s)]["avg"] for s in xs]
        ax.plot(xs, ys, marker="o", linewidth=2.5, markersize=8, label=algo, color=color)
    ax.set_title("Tempo Médio x Tamanho do Vetor", color="white", fontsize=14, pad=15)
    ax.set_xlabel("Tamanho (n)", color="#AAAAAA")
    ax.set_ylabel("Tempo Médio (s)", color="#AAAAAA")
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(fmt_n)
    _legend(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "grafico_tempo_medio_linha.png"), dpi=150)
    plt.close()

    # 2. Barras Agrupadas
    fig, ax = plt.subplots(figsize=(12, 6))
    _dark_ax(fig, ax)
    bar_w = 0.22
    xs = range(len(SIZES))
    for i, (algo, color) in enumerate(PALETTE.items()):
        avgs = [results[(algo, s)]["avg"] for s in SIZES]
        offsets = [x + (i - 1) * bar_w for x in xs]
        ax.bar(offsets, avgs, width=bar_w, label=algo, color=color, alpha=0.85)
    ax.set_title("Comparação de Tempo Médio por Tamanho", color="white", fontsize=13)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{s:,}" for s in SIZES])
    _legend(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "grafico_barras_agrupadas.png"), dpi=150)
    plt.close()

    # 3. Trocas/Movimentações x Tamanho
    fig, ax = plt.subplots(figsize=(10, 6))
    _dark_ax(fig, ax)
    for algo, color in PALETTE.items():
        xs = SIZES
        ys = [results[(algo, s)]["avg_ops"] for s in xs]
        ax.plot(xs, ys, marker="s", linewidth=2.5, label=algo, color=color, linestyle="--")
    ax.set_title("Trocas / Movimentações x Tamanho", color="white", fontsize=14)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.xaxis.set_major_formatter(fmt_n)
    ax.yaxis.set_major_formatter(fmt_n)
    _legend(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "grafico_trocas_movimentacoes.png"), dpi=150)
    plt.close()

    # 4. Log-log com barras de desvio padrão
    fig, ax = plt.subplots(figsize=(10, 6))
    _dark_ax(fig, ax)
    for algo, color in PALETTE.items():
        xs  = SIZES
        ys  = [results[(algo, s)]["avg"] for s in xs]
        err = [results[(algo, s)]["std"] for s in xs]
        ax.errorbar(xs, ys, yerr=err, marker="o", label=algo, color=color, capsize=5)
    ax.set_title("Tempo Médio (log-log) com Desvio Padrão", color="white", fontsize=14)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.xaxis.set_major_formatter(fmt_n)
    _legend(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "grafico_loglog_desvpad.png"), dpi=150)
    plt.close()

if __name__ == "__main__":
    results = run_benchmarks()
    export_csv(results, "resultados_benchmark.csv")
    make_graphs(results, "graficos")
