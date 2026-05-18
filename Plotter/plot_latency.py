import csv
import os
import sys
import math

import matplotlib.pyplot as plt
import numpy as np

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data\latency_results.csv")
OUT_DIR = os.path.dirname(__file__)

def load_data(path):
    timestamps = []
    latencies = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(row["Timestamp"])
            latencies.append(float(row["Latency_ms"]))
    return timestamps, latencies

def compute_stats(latencies):
    arr = np.array(latencies)
    return {
        "count": len(arr),
        "mean": np.mean(arr),
        "median": np.median(arr),
        "std": np.std(arr, ddof=1),
        "min": np.min(arr),
        "max": np.max(arr),
        "p99": np.percentile(arr, 99),
        "p95": np.percentile(arr, 95),
    }

def plot_timeseries(latencies, stats, out_dir):
    fig, ax = plt.subplots(figsize=(10, 4))
    packets = np.arange(1, len(latencies) + 1)
    ax.plot(packets, latencies, color="#2196F3", linewidth=0.8, alpha=0.8)
    ax.axhline(stats["mean"], color="#F44336", linestyle="--", linewidth=1,
               label=f'Mean = {stats["mean"]:.2f} ms')
    ax.axhline(stats["min"], color="#4CAF50", linestyle=":", linewidth=1,
               label=f'Min = {stats["min"]:.2f} ms')
    ax.axhline(stats["max"], color="#FF9800", linestyle=":", linewidth=1,
               label=f'Max = {stats["max"]:.2f} ms')
    ax.set_xlabel("Packet Number")
    ax.set_ylabel("Latency (ms)")
    ax.set_title("UDP Round-Trip Latency per Packet")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "latency_timeseries.png"), dpi=150)
    plt.close(fig)
    print("  Saved: latency_timeseries.png")

def plot_histogram(latencies, stats, out_dir):
    fig, ax = plt.subplots(figsize=(8, 4))
    bins = int(math.sqrt(len(latencies))) * 2
    ax.hist(latencies, bins=bins, color="#2196F3", edgecolor="white", alpha=0.85)
    ax.axvline(stats["mean"], color="#F44336", linestyle="--", linewidth=1.5,
               label=f'Mean = {stats["mean"]:.2f} ms')
    ax.axvline(stats["median"], color="#9C27B0", linestyle="-.", linewidth=1.5,
               label=f'Median = {stats["median"]:.2f} ms')
    ax.set_xlabel("Latency (ms)")
    ax.set_ylabel("Frequency")
    ax.set_title("Latency Distribution")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "latency_histogram.png"), dpi=150)
    plt.close(fig)
    print("  Saved: latency_histogram.png")

def plot_box(latencies, stats, out_dir):
    fig, ax = plt.subplots(figsize=(6, 4))
    bp = ax.boxplot(latencies, vert=True, patch_artist=True,
                    boxprops=dict(facecolor="#2196F3", alpha=0.7),
                    medianprops=dict(color="#F44336", linewidth=2),
                    flierprops=dict(marker="o", markerfacecolor="#FF9800",
                                    markersize=5, alpha=0.6))
    ax.set_ylabel("Latency (ms)")
    ax.set_xticklabels(["All Packets"])
    ax.set_title("Latency Box Plot")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "latency_boxplot.png"), dpi=150)
    plt.close(fig)
    print("  Saved: latency_boxplot.png")

def plot_cdf(latencies, out_dir):
    fig, ax = plt.subplots(figsize=(8, 4))
    sorted_data = np.sort(latencies)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    ax.plot(sorted_data, cdf, color="#2196F3", linewidth=1.5)
    ax.axhline(0.95, color="#F44336", linestyle="--", linewidth=1,
               label="95th percentile")
    ax.axhline(0.99, color="#FF9800", linestyle=":", linewidth=1,
               label="99th percentile")
    ax.set_xlabel("Latency (ms)")
    ax.set_ylabel("Cumulative Probability")
    ax.set_title("CDF of Latency")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "latency_cdf.png"), dpi=150)
    plt.close(fig)
    print("  Saved: latency_cdf.png")

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found")
        sys.exit(1)

    print(f"Loading data from: {CSV_PATH}")
    timestamps, latencies = load_data(CSV_PATH)
    stats = compute_stats(latencies)

    print(f"\n{'='*45}")
    print(f"  Latency Test Results  (n = {stats['count']})")
    print(f"{'='*45}")
    print(f"  Mean    : {stats['mean']:.2f} ms")
    print(f"  Median  : {stats['median']:.2f} ms")
    print(f"  Std Dev : {stats['std']:.2f} ms")
    print(f"  Min     : {stats['min']:.2f} ms")
    print(f"  Max     : {stats['max']:.2f} ms")
    print(f"  P95     : {stats['p95']:.2f} ms")
    print(f"  P99     : {stats['p99']:.2f} ms")
    print(f"{'='*45}\n")

    os.makedirs(OUT_DIR, exist_ok=True)
    print("Generating plots...")
    plot_timeseries(latencies, stats, OUT_DIR)
    plot_histogram(latencies, stats, OUT_DIR)
    plot_box(latencies, stats, OUT_DIR)
    plot_cdf(latencies, OUT_DIR)
    print(f"\nAll plots saved to: {OUT_DIR}/")

if __name__ == "__main__":
    main()
