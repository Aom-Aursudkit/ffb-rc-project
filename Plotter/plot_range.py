import csv
import os

import matplotlib.pyplot as plt
import numpy as np

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "range_results.csv")
OUT_DIR = os.path.join(os.path.dirname(__file__), "plot_result")

def load_filtered():
    rows = []
    with open(CSV_PATH, newline="") as f:
        for r in csv.DictReader(f):
            d = int(r["Distance_m"])
            if d in (10, 20, 30, 40):
                rows.append({
                    "dist": d,
                    "lat": float(r["Avg_Latency_ms"]),
                    "loss": float(r["Packet_Loss_Percent"]),
                    "min": float(r["Min_Latency_ms"]),
                    "max": float(r["Max_Latency_ms"]),
                })
    return sorted(rows, key=lambda x: x["dist"])

def plot_latency(rows):
    fig, ax = plt.subplots(figsize=(7, 4))
    dists = [r["dist"] for r in rows]
    latencies = [r["lat"] for r in rows]

    ax.bar(dists, latencies, width=5, color="#2196F3", edgecolor="white", alpha=0.85)
    ax.axhline(70, color="#F44336", linestyle="--", linewidth=1.2, label="70 ms threshold")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Average Latency (ms)")
    ax.set_title("UDP Latency vs Distance")
    ax.set_xticks(dists)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    for r, lat in zip(rows, latencies):
        ax.text(r["dist"], lat + 0.3, f"{lat:.2f}", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "range_latency.png"), dpi=150)
    plt.close(fig)
    print("  Saved: range_latency.png")

def plot_packet_loss(rows):
    fig, ax = plt.subplots(figsize=(7, 4))
    dists = [r["dist"] for r in rows]
    losses = [r["loss"] for r in rows]

    ax.bar(dists, losses, width=5, color="#FF9800", edgecolor="white", alpha=0.85)
    ax.axhline(5, color="#F44336", linestyle="--", linewidth=1.2, label="5% threshold")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Packet Loss (%)")
    ax.set_title("Packet Loss vs Distance")
    ax.set_xticks(dists)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    for r, loss in zip(rows, losses):
        ax.text(r["dist"], loss + 0.05, f"{loss:.2f}%", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "range_packet_loss.png"), dpi=150)
    plt.close(fig)
    print("  Saved: range_packet_loss.png")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = load_filtered()
    print(f"Loaded {len(rows)} distance points: {[r['dist'] for r in rows]}")
    plot_latency(rows)
    plot_packet_loss(rows)
    print(f"All plots saved to: {OUT_DIR}/")

if __name__ == "__main__":
    main()