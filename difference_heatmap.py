#!/usr/bin/env python3
"""
difference_heatmap.py

Creates a heatmap comparing all evaluation metrics.
"""

import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np


LABELS = {
    "dsp_only": "DSP",
    "generative": "Generative",
    "combined": "Combined",
}


def load_results(path):
    with open(path) as f:
        raw = json.load(f)

    if isinstance(raw, list):
        return {entry["condition"]: entry for entry in raw}

    return raw


def normalise(values, higher_better=True):
    values = np.asarray(values, dtype=float)

    if np.allclose(values.max(), values.min()):
        return np.ones_like(values)

    if higher_better:
        return (values - values.min()) / (values.max() - values.min())

    return (values.max() - values) / (values.max() - values.min())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="difference_heatmap.png")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    data = load_results(args.input)

    metrics = [
        ("si_sdr_mix_db", True, "SI-SDR Mix"),
        ("si_sdr_dialogue_db", True, "SI-SDR Dialogue"),
        ("pesq_wb", True, "PESQ"),
        ("stoi", True, "STOI"),
        ("spectral_centroid_shift_hz", False, "Spectral Shift"),
        ("transient_peak_reduction_db", True, "Transient Reduction"),
        ("rdir_improvement", True, "RDIR"),
    ]

    methods = [c for c in ["dsp_only", "generative", "combined"] if c in data]

    matrix = []
    row_labels = []

    for key, higher, label in metrics:
        vals = [data[method][key] for method in methods]
        matrix.append(normalise(vals, higher))
        row_labels.append(label)

    matrix = np.asarray(matrix)

    fig, ax = plt.subplots(figsize=(8, 6), facecolor="#0F1117")
    ax.set_facecolor("#1A1D27")

    im = ax.imshow(
        matrix,
        cmap="RdYlGn",
        aspect="auto",
        vmin=0,
        vmax=1
    )

    ax.set_xticks(np.arange(len(methods)))
    ax.set_xticklabels(
        [LABELS.get(m, m) for m in methods],
        color="white",
        fontsize=11,
        fontweight="bold"
    )

    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(
        row_labels,
        color="white",
        fontsize=10
    )

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(
                j,
                i,
                f"{matrix[i, j]:.2f}",
                ha="center",
                va="center",
                color="black",
                fontsize=9,
                fontweight="bold"
            )

    for spine in ax.spines.values():
        spine.set_color("#2A2D3A")

    cbar = plt.colorbar(im)
    cbar.set_label("Normalised Performance", color="white")
    cbar.ax.tick_params(colors="white")

    plt.title(
        "Objective Metric Comparison",
        color="white",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    plt.tight_layout()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    plt.savefig(
        args.output,
        dpi=args.dpi,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close()
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
