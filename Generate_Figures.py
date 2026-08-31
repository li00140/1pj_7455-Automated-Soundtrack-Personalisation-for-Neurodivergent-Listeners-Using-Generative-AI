"""
EEEM004 MSc Project — Pipeline Diagram Generator
Generates Figure 1 (Demucs pipeline) and Figure 3 (SAM Audio pipeline)
as publication-quality PNG files suitable for the dissertation.

Run with:
    python generate_pipeline_figures.py

Output:
    figure1_demucs_pipeline.png
    figure3_samaudio_pipeline.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ── Shared style ──────────────────────────────────────────────────────────────

FONT = "DejaVu Sans"
DPI  = 200

# Colour palette
C_BOX      = "#1A3A5C"   # dark navy — main process boxes
C_BOX_STEM = "#2E6DA4"   # mid blue — stems / outputs
C_BOX_MIX  = "#1B6B3A"   # dark green — final mix output
C_BOX_IN   = "#4A4A4A"   # dark grey — input
C_BOX_PROMPT = "#7B3F00" # brown — text prompt
C_ARROW    = "#444444"
C_BG       = "#F8F9FB"
C_TEXT     = "white"
C_LABEL    = "#1A1A2E"


def draw_box(ax, x, y, w, h, label, sublabel=None,
             color=C_BOX, fontsize=9, sublabel_size=7.5):
    """Draw a rounded rectangle with centred text."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02",
        linewidth=1.2,
        edgecolor="white",
        facecolor=color,
        zorder=3
    )
    ax.add_patch(box)
    if sublabel:
        ax.text(x, y + 0.055, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=C_TEXT,
                fontfamily=FONT, zorder=4)
        ax.text(x, y - 0.065, sublabel, ha="center", va="center",
                fontsize=sublabel_size, color="#CCDDEE",
                fontfamily=FONT, zorder=4, style="italic")
    else:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", color=C_TEXT,
                fontfamily=FONT, zorder=4)


def arrow(ax, x0, y0, x1, y1, label=None):
    """Draw an arrow between two points."""
    ax.annotate(
        "", xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(
            arrowstyle="->,head_width=0.18,head_length=0.10",
            color=C_ARROW, lw=1.4
        ),
        zorder=2
    )
    if label:
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ax.text(mx + 0.02, my, label, fontsize=7, color="#555555",
                fontfamily=FONT, va="center", style="italic")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Demucs-based pipeline
# ═══════════════════════════════════════════════════════════════════════════════

def make_figure1():
    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    ax.text(6.5, 5.1, "Figure 1 — Demucs-Based Separation Pipeline",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=C_LABEL, fontfamily=FONT)

    # ── Row 1: Input → Demucs → four stems ────────────────────────────────

    # Input audio
    draw_box(ax, 1.1, 3.2, 1.6, 0.55, "Input Audio", "(Mixed Soundtrack)",
             color=C_BOX_IN, fontsize=9)

    # Arrow to Demucs
    arrow(ax, 1.92, 3.2, 2.55, 3.2)

    # Demucs
    draw_box(ax, 3.25, 3.2, 1.3, 0.55, "Demucs", "htdemucs model",
             color=C_BOX, fontsize=9)

    # Fan-out arrows to four stems
    stems = [
        (5.5, 4.55, "#2E6DA4", "Vocals stem\n(≈ Dialogue)"),
        (5.5, 3.5,  "#2E6DA4", "Other stem\n(≈ Background)"),
        (5.5, 2.45, "#555577", "Drums stem"),
        (5.5, 1.4,  "#555577", "Bass stem"),
    ]
    for sx, sy, sc, sl in stems:
        arrow(ax, 3.92, 3.2, 4.85, sy)
        lines = sl.split("\n")
        top = lines[0]
        bot = lines[1] if len(lines) > 1 else None
        draw_box(ax, sx, sy, 1.55, 0.48, top, bot,
                 color=sc, fontsize=8.5, sublabel_size=7.2)

    # ── Row 2: Vocals → noisereduce → enhanced vocals ─────────────────────

    arrow(ax, 6.28, 4.55, 7.15, 4.55)
    draw_box(ax, 7.85, 4.55, 1.35, 0.48, "noisereduce", "post-processing",
             color="#1A4A6B", fontsize=8.5)
    arrow(ax, 8.53, 4.55, 9.35, 4.55)
    draw_box(ax, 10.0, 4.55, 1.35, 0.48, "Enhanced\nVocals", None,
             color=C_BOX_STEM, fontsize=8.5)

    # ── Row 3: pyannote diarization on vocals ─────────────────────────────

    arrow(ax, 6.28, 4.55, 7.15, 3.7)
    draw_box(ax, 7.85, 3.7, 1.35, 0.48, "pyannote.audio", "diarization",
             color="#1A4A6B", fontsize=8.5)
    arrow(ax, 8.53, 3.7, 9.35, 3.7)
    draw_box(ax, 10.0, 3.7, 1.35, 0.48, "Speaker\nSegments", None,
             color=C_BOX_STEM, fontsize=8.5)

    # ── Row 4: Other stem + Enhanced vocals → personalised mix ───────────

    # Arrow from other stem rightward to mixer area
    arrow(ax, 6.28, 3.5, 9.35, 2.65)

    # Arrow from enhanced vocals down to mixer
    arrow(ax, 10.0, 4.32, 10.0, 2.98)

    # Mixer symbol (circle)
    circle = plt.Circle((10.0, 2.65), 0.24, color="#2A5A3C",
                         ec="white", lw=1.2, zorder=3)
    ax.add_patch(circle)
    ax.text(10.0, 2.65, "+", ha="center", va="center",
            fontsize=14, color="white", fontweight="bold",
            fontfamily=FONT, zorder=4)

    ax.text(10.0, 2.28, "gain-boost dialogue\ngain-reduce background",
            ha="center", va="center", fontsize=6.8,
            color="#444", fontfamily=FONT, style="italic")

    # Final personalised mix
    arrow(ax, 10.24, 2.65, 11.1, 2.65)
    draw_box(ax, 11.9, 2.65, 1.5, 0.52, "Personalised Mix", "(WAV output)",
             color=C_BOX_MIX, fontsize=9)

    # ── Unused stems note ─────────────────────────────────────────────────
    ax.text(5.5, 0.75, "Note: Drums and Bass stems not used in personalisation "
            "(musical source categories, irrelevant to this application)",
            ha="center", va="center", fontsize=7.5,
            color="#888", fontfamily=FONT, style="italic")

    # ── Limitation callout ────────────────────────────────────────────────
    lim = FancyBboxPatch((0.15, 0.1), 4.2, 0.55,
                          boxstyle="round,pad=0.02",
                          facecolor="#FFF3CD", edgecolor="#CCAA00",
                          linewidth=1, zorder=3)
    ax.add_patch(lim)
    ax.text(2.25, 0.37,
            "⚠  Limitation: Demucs separates into musical stems\n"
            "(vocals/drums/bass/other), not dialogue/music/SFX directly.",
            ha="center", va="center", fontsize=7.5,
            color="#7A5900", fontfamily=FONT, zorder=4)

    plt.tight_layout(pad=0.3)
    plt.savefig("figure1_demucs_pipeline.png", dpi=DPI,
                bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print("Saved: figure1_demucs_pipeline.png")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — SAM Audio pipeline
# ═══════════════════════════════════════════════════════════════════════════════

def make_figure3():
    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    ax.text(6.5, 5.1, "Figure 3 — SAM Audio Text-Prompted Separation Pipeline",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=C_LABEL, fontfamily=FONT)

    # ── Input audio ───────────────────────────────────────────────────────
    draw_box(ax, 1.1, 2.75, 1.6, 0.55, "Input Audio", "(Mixed Soundtrack)",
             color=C_BOX_IN, fontsize=9)

    # ── Text prompts (fan-in from left) ───────────────────────────────────
    prompts = [
        (1.1, 4.3,  '"a person speaking"'),
        (1.1, 3.55, '"background music"'),
        (1.1, 1.95, '"sound effects\nand ambient noise"'),
    ]
    for px, py, pt in prompts:
        lines = pt.split("\n")
        draw_box(ax, px, py, 1.9, 0.44 if len(lines) == 1 else 0.52,
                 lines[0], lines[1] if len(lines) > 1 else None,
                 color=C_BOX_PROMPT, fontsize=8, sublabel_size=7.5)

    # ── SAM Audio model (central) ─────────────────────────────────────────

    # Arrows: input audio → SAM Audio (3 times, one per separation)
    for py in [4.3, 3.55, 1.95]:
        arrow(ax, 2.05, 2.75, 3.55, py)   # from input
        arrow(ax, 2.06, py,   3.55, py)   # from prompt

    draw_box(ax, 4.2, 4.3,  1.3, 0.48, "SAM Audio", "facebook/sam-audio-small",
             color=C_BOX, fontsize=8.5)
    draw_box(ax, 4.2, 3.55, 1.3, 0.48, "SAM Audio", "facebook/sam-audio-small",
             color=C_BOX, fontsize=8.5)
    draw_box(ax, 4.2, 1.95, 1.3, 0.48, "SAM Audio", "facebook/sam-audio-small",
             color=C_BOX, fontsize=8.5)

    # Label showing it's the same model called three times
    ax.annotate("", xy=(4.85, 1.72), xytext=(4.85, 4.55),
                arrowprops=dict(arrowstyle="-",
                                color="#AAAAAA", lw=1,
                                linestyle="dashed"))
    ax.text(5.12, 3.1, "same\nmodel", ha="center", va="center",
            fontsize=6.5, color="#AAAAAA", fontfamily=FONT, style="italic",
            rotation=90)

    # ── Outputs: target + residual pairs ─────────────────────────────────

    rows = [
        (4.3,  "Dialogue Target", "Dialogue Residual"),
        (3.55, "Music Target",    "Music Residual"),
        (1.95, "SFX Target",      "SFX Residual"),
    ]
    for (py, tlabel, rlabel) in rows:
        arrow(ax, 4.86, py, 5.7, py + 0.25)   # target
        arrow(ax, 4.86, py, 5.7, py - 0.25)   # residual
        draw_box(ax, 6.55, py + 0.25, 1.6, 0.42, tlabel, None,
                 color=C_BOX_STEM, fontsize=8)
        draw_box(ax, 6.55, py - 0.25, 1.6, 0.42, rlabel, None,
                 color="#3D3D5C", fontsize=8)

    # ── Personalised mix stage ────────────────────────────────────────────

    # Arrows from dialogue target and residual into mixer
    arrow(ax, 7.36, 4.55, 8.8, 3.5)   # dialogue target
    arrow(ax, 7.36, 4.05, 8.8, 3.35)  # dialogue residual

    # Mixer
    circle = plt.Circle((9.1, 3.15), 0.28, color="#2A5A3C",
                         ec="white", lw=1.2, zorder=3)
    ax.add_patch(circle)
    ax.text(9.1, 3.15, "+", ha="center", va="center",
            fontsize=14, color="white", fontweight="bold",
            fontfamily=FONT, zorder=4)

    ax.text(9.1, 2.72, "dialogue × boost\nresidual × reduce",
            ha="center", va="center", fontsize=6.8,
            color="#444", fontfamily=FONT, style="italic")

    # Final output
    arrow(ax, 9.38, 3.15, 10.3, 3.15)
    draw_box(ax, 11.1, 3.15, 1.5, 0.52, "Personalised Mix", "(WAV output)",
             color=C_BOX_MIX, fontsize=9)

    # ── Advantage callout ─────────────────────────────────────────────────
    adv = FancyBboxPatch((0.15, 0.1), 5.5, 0.55,
                          boxstyle="round,pad=0.02",
                          facecolor="#D4EDDA", edgecolor="#28A745",
                          linewidth=1, zorder=3)
    ax.add_patch(adv)
    ax.text(2.9, 0.37,
            "✓  Advantage over Demucs: text prompts directly target\n"
            "   dialogue, music and SFX — no indirect stem mapping required.",
            ha="center", va="center", fontsize=7.5,
            color="#155724", fontfamily=FONT, zorder=4)

    # ── Legend ────────────────────────────────────────────────────────────
    legend_items = [
        (C_BOX_IN,     "Input"),
        (C_BOX_PROMPT, "Text prompt"),
        (C_BOX,        "SAM Audio model"),
        (C_BOX_STEM,   "Target stem"),
        ("#3D3D5C",    "Residual stem"),
        (C_BOX_MIX,    "Personalised output"),
    ]
    lx, ly = 7.8, 1.1
    for i, (col, lbl) in enumerate(legend_items):
        bx = lx + (i % 3) * 1.65
        by = ly - (i // 3) * 0.38
        rect = FancyBboxPatch((bx, by - 0.12), 0.22, 0.24,
                               boxstyle="round,pad=0.01",
                               facecolor=col, edgecolor="white",
                               linewidth=0.8, zorder=3)
        ax.add_patch(rect)
        ax.text(bx + 0.28, by, lbl, ha="left", va="center",
                fontsize=7, color=C_LABEL, fontfamily=FONT, zorder=4)

    plt.tight_layout(pad=0.3)
    plt.savefig("figure3_samaudio_pipeline.png", dpi=DPI,
                bbox_inches="tight", facecolor=C_BG)
    plt.close()
    print("Saved: figure3_samaudio_pipeline.png")


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    make_figure1()
    make_figure3()
    print("\nDone. Both figures saved to the current directory.")