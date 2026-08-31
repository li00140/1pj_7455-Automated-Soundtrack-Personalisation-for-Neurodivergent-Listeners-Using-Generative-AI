#!/usr/bin/env python3

"""
spectrograms.py
-----------------------------------------
Generate publication-quality spectrogram
comparison figures for all four processing
conditions.

Usage:

python spectrograms.py \
    --baseline baseline.wav \
    --dsp dsp.wav \
    --generative generative.wav \
    --combined combined.wav \
    --output spectrograms.png
"""

import argparse
import os

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def load_audio(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    y, sr = librosa.load(path, sr=None, mono=True)

    return y, sr


def compute_mel_spectrogram(y, sr):

    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=2048,
        hop_length=512,
        n_mels=128,
        power=2,
    )

    mel_db = librosa.power_to_db(
        mel,
        ref=np.max
    )

    return mel_db


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--baseline", required=True)
    parser.add_argument("--dsp", required=True)
    parser.add_argument("--generative", required=True)
    parser.add_argument("--combined", required=True)

    parser.add_argument(
        "--output",
        default="spectrogram_comparison.png"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=300
    )

    args = parser.parse_args()

    files = {
        "Baseline": args.baseline,
        "DSP": args.dsp,
        "Generative": args.generative,
        "Combined": args.combined,
    }

    colours = {
        "Baseline": "#B0B0B0",
        "DSP": "#4C9BE8",
        "Generative": "#E8824C",
        "Combined": "#6FCF97",
    }

    audio = {}
    specs = []

    # --------------------------------------------
    # Load audio
    # --------------------------------------------

    for name, path in files.items():

        y, sr = load_audio(path)

        S = compute_mel_spectrogram(y, sr)

        audio[name] = {
            "audio": y,
            "sr": sr,
            "spec": S,
        }

        specs.append(S)

    # Shared colour scale
    global_min = min(np.min(s) for s in specs)
    global_max = max(np.max(s) for s in specs)

    # --------------------------------------------
    # Figure
    # --------------------------------------------

    fig = plt.figure(
        figsize=(15, 14),
        facecolor="#0F1117"
    )

    fig.suptitle(
        "EEEM004 Processing Comparison\nMel Spectrograms",
        fontsize=18,
        color="white",
        fontweight="bold",
    )

    gs = gridspec.GridSpec(
        4,
        1,
        hspace=0.35
    )

    panel_bg = "#1A1D27"
    grid_color = "#2A2D3A"
    text_color = "#C8CDD8"

    axes = []

    for i, name in enumerate(audio):

        ax = fig.add_subplot(gs[i])

        ax.set_facecolor(panel_bg)

        spec = librosa.display.specshow(
            audio[name]["spec"],
            sr=audio[name]["sr"],
            hop_length=512,
            x_axis="time",
            y_axis="mel",
            cmap="magma",
            vmin=global_min,
            vmax=global_max,
            ax=ax,
        )

        ax.set_title(
            name,
            color=colours[name],
            fontsize=13,
            fontweight="bold",
            loc="left"
        )

        ax.tick_params(
            colors=text_color,
            labelsize=9
        )

        for spine in ax.spines.values():
            spine.set_color(grid_color)

        ax.set_xlabel("")

        axes.append(ax)

    axes[-1].set_xlabel(
        "Time (s)",
        color=text_color,
        fontsize=11
    )

    cbar = fig.colorbar(
        spec,
        ax=axes,
        pad=0.02,
        shrink=0.98
    )

    cbar.set_label(
        "Level (dB)",
        color=text_color,
        fontsize=11
    )

    cbar.ax.yaxis.set_tick_params(
        color=text_color
    )

    plt.setp(
        plt.getp(cbar.ax.axes, "yticklabels"),
        color=text_color
    )

    plt.savefig(
        args.output,
        dpi=args.dpi,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    plt.close()

    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
