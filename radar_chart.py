#!/usr/bin/env python3
"""
radar_chart.py

Generate a radar/spider chart comparing processing conditions.
"""

import argparse
import json
import os

import numpy as np
import matplotlib.pyplot as plt


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


def normalise(values, higher_is_better=True):
    values = np.asarray(values, dtype=float)

    if np.allclose(values.max(), values.min()):
        return np.ones_like(values)

    if higher_is_better:
        return (values - values.min()) / (values.max() - values.min())

    return (values.max() - values) / (values.max() - values.min())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="radar_chart.png")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    data = load_results(args.input)

    metrics = [
        ("si_sdr_mix_db", True, "SI-SDR\nMix"),
        ("si_sdr_dialogue_db", True, "SI-SDR\nDialogue"),
        ("pesq_wb", True, "PESQ"),
        ("stoi", True, "STOI"),
        ("spectral_centroid_shift_hz", False, "Spectral\nShift"),
        ("transient_peak_reduction_db", True, "Transient\nReduction"),
        ("rdir_improvement", True, "RDIR"),
    ]

    conditions = [c for c in ["dsp_only", "generative", "combined"] if c in data]

    values = {cond: [] for cond in conditions}

    for metric, higher, _ in metrics:
        raw_vals = [data[cond][metric] for cond in conditions]
        norm_vals = normalise(raw_vals, higher)

        for cond, value in zip(conditions, norm_vals):
            values[cond].append(value)

    labels = [m[2] for m in metrics]
    n = len(labels)

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig = plt.figure(figsize=(8, 8), facecolor="#0F1117")
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor("#1A1D27")

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color="#C8CDD8", fontsize=10)

    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.grid(color="#2A2D3A", alpha=0.6)
    ax.spines["polar"].set_color("#2A2D3A")

    for cond in conditions:
        vals = values[cond] + values[cond][:1]
        colour = COLORS.get(cond, "#999999")

        ax.plot(
            angles,
            vals,
            linewidth=2,
            color=colour,
            label=LABELS.get(cond, cond)
        )

        ax.fill(
            angles,
            vals,
            alpha=0.25,
            color=colour
        )

    plt.title(
        "Normalised Objective Metrics",
        fontsize=16,
        color="white",
        fontweight="bold",
        pad=20
    )

    legend = plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.10),
        frameon=False
    )

    for text in legend.get_texts():
        text.set_color("white")

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
