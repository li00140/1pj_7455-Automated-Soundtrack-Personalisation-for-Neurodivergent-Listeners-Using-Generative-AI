#!/usr/bin/env python3
"""
metrics_barplot.py

Generate publication-quality bar charts from evaluation_results.json.
"""

import argparse
import json
import math
import os

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


COLORS = {
    "dsp_only": "#4C9BE8",
    "generative": "#E8824C",
    "combined": "#6FCF97",
}

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="metrics_barplot.png")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    data = load_results(args.input)

    metrics = [
        ("si_sdr_mix_db", "SI-SDR Mix (dB)", True),
        ("si_sdr_dialogue_db", "SI-SDR Dialogue (dB)", True),
        ("pesq_wb", "PESQ-WB", True),
        ("stoi", "STOI", True),
        ("spectral_centroid_shift_hz", "Spectral Shift (Hz)", False),
        ("transient_peak_reduction_db", "Transient Reduction (dB)", True),
        ("rdir_improvement", "RDIR Improvement", True),
    ]

    conditions = [c for c in ["dsp_only", "generative", "combined"] if c in data]

    fig = plt.figure(figsize=(14, 10), facecolor="#0F1117")
    fig.suptitle(
        "Objective Evaluation Metrics",
        fontsize=18,
        color="white",
        fontweight="bold"
    )

    rows = math.ceil(len(metrics) / 3)
    gs = gridspec.GridSpec(rows, 3, hspace=0.45, wspace=0.35)

    panel = "#1A1D27"
    grid = "#2A2D3A"
    text = "#C8CDD8"

    for i, (key, title, higher_better) in enumerate(metrics):
        ax = fig.add_subplot(gs[i])
        ax.set_facecolor(panel)

        labels = [LABELS.get(c, c) for c in conditions]
        values = [data[c].get(key) for c in conditions]
        colours = [COLORS.get(c, "#999999") for c in conditions]

        bars = ax.bar(labels, values, color=colours, width=0.6)

        direction = "↑ better" if higher_better else "↓ better"
        ax.set_title(
            f"{title} ({direction})",
            color="white",
            fontsize=10,
            fontweight="bold"
        )

        ax.grid(axis="y", alpha=0.35, color=grid)
        ax.tick_params(colors=text)

        for spine in ax.spines.values():
            spine.set_color(grid)

        for bar, value in zip(bars, values):
            if value is None:
                continue

            h = bar.get_height()
            va = "bottom" if h >= 0 else "top"
            offset = abs(h) * 0.03 if abs(h) > 1e-9 else 0.03

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + offset if h >= 0 else h - offset,
                f"{value:.2f}",
                ha="center",
                va=va,
                fontsize=8,
                color=text
            )

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
