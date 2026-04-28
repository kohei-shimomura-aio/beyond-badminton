"""
Generate figures for the Beyond Badminton submission PDF.
Creates: system diagram, pattern timeline, comparison charts,
keyword bar charts.
"""
import os
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

# Output folder
HERE = Path(__file__).parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)

# Theme colors
COLOR_BG = "#f8fafc"
COLOR_PRIMARY = "#6366f1"      # indigo
COLOR_ACCENT = "#10b981"       # green
COLOR_HIGHLIGHT = "#f59e0b"    # amber
COLOR_DANGER = "#ef4444"       # red
COLOR_TEXT = "#0f172a"         # slate-900
COLOR_MUTED = "#64748b"        # slate-500


# =============================================================
# Figure 1: System architecture diagram
# =============================================================
def fig_system_diagram():
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x, y, w, h, label, color, sub=""):
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            linewidth=2, edgecolor=color, facecolor="white",
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2 + (0.15 if sub else 0),
                label, ha="center", va="center",
                fontsize=11, fontweight="bold", color=color)
        if sub:
            ax.text(x + w / 2, y + h / 2 - 0.18, sub,
                    ha="center", va="center",
                    fontsize=8, color=COLOR_MUTED)

    def arrow(x1, y1, x2, y2, label="", offset=0.2):
        a = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="->", mutation_scale=20,
            linewidth=1.5, color=COLOR_TEXT,
        )
        ax.add_patch(a)
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + offset, label,
                    ha="center", va="center", fontsize=8.5,
                    color=COLOR_MUTED, style="italic")

    # Top: Configuration (yaml)
    box(0.3, 5.5, 2.4, 1.0, "config.yaml", COLOR_PRIMARY,
        "field, places, personas,\nannouncements")

    # Center: Simulation core
    box(4.6, 5.5, 2.8, 1.0, "Simulation", COLOR_ACCENT,
        "20 agents, step loop\ncapacity enforcement")

    # Right: LLM service
    box(9.0, 5.5, 2.7, 1.0, "Ollama + gemma4:e4b", COLOR_HIGHLIGHT,
        "JSON-mode inference\nthink:false, num_ctx 2048")

    arrow(2.7, 6.0, 4.6, 6.0, "load")
    arrow(7.4, 6.0, 9.0, 6.0, "prompt / response")
    arrow(9.0, 5.5, 7.4, 5.5)  # back arrow

    # Middle: Agents (20)
    box(4.6, 3.4, 2.8, 1.4, "20 LLM Agents", COLOR_PRIMARY,
        "personas (6 archetypes)\ngender 10 male / 10 female\nposition · memory · messages")
    arrow(6.0, 5.5, 6.0, 4.8, "")

    # Left: Place (court / arena)
    box(0.3, 3.4, 2.4, 1.4, "1 Place", COLOR_ACCENT,
        "rectangular arena\n3×7 court (real ratio)\ncapacity 6")
    arrow(2.7, 4.1, 4.6, 4.1, "spatial context")

    # Right: Announcement / Hazard system
    box(9.0, 3.4, 2.7, 1.4, "Event System", COLOR_HIGHLIGHT,
        "announcements (PA system)\nhazards (off in P5–7)")
    arrow(9.0, 4.1, 7.4, 4.1, "events")

    # Bottom: Output
    box(0.3, 1.0, 3.0, 1.4, "Output / Logs", COLOR_DANGER,
        "messages.jsonl\nmemory_reasoning.jsonl\nframe_*.png · statistics")
    arrow(6.0, 3.4, 1.8, 2.4, "")

    # Bottom: Visualizer
    box(4.6, 1.0, 2.8, 1.4, "Visualizer", COLOR_PRIMARY,
        "matplotlib renderer\nphase indicator · roles\nbadminton court markings")
    arrow(6.0, 3.4, 6.0, 2.4, "frames")

    # Bottom: Viewer (browser)
    box(8.6, 1.0, 3.1, 1.4, "Browser Viewer", COLOR_ACCENT,
        "viewer.html (interactive)\nphase progress bar\nmessage / memory panels")
    arrow(7.4, 1.7, 8.6, 1.7, "playback")

    ax.text(6.0, 6.8, "Beyond Badminton — System Architecture",
            ha="center", fontsize=14, fontweight="bold", color=COLOR_TEXT)

    plt.tight_layout()
    out = FIG / "01_system_diagram.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=COLOR_BG)
    plt.close()
    print(f"[OK] {out}")


# =============================================================
# Figure 2: Pattern timeline
# =============================================================
def fig_pattern_timeline():
    fig, ax = plt.subplots(figsize=(12, 4.5))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    patterns = [
        ("Pattern 1", "qwen2.5/JP\nradius 3", "Philosophical drift",
         COLOR_DANGER, "Failure"),
        ("Pattern 2", "e2b/JP\nradius 2", "Static / no comms",
         COLOR_DANGER, "Failure"),
        ("Pattern 3", "e2b/JP\nintervention", "Partial emergence",
         COLOR_HIGHLIGHT, "Mild"),
        ("Pattern 4", "e2b/JP\nno hazards", "Eternal warm-up",
         COLOR_HIGHLIGHT, "Stuck"),
        ("Pattern 5", "e4b/EN\nrect courts", "Sport reconstruction\n(coach role!)",
         COLOR_ACCENT, "Success"),
        ("Pattern 6", "e4b/EN\npersonas + PA", "Group drama\n+ FAN culture (1138 cheers!)",
         COLOR_ACCENT, "Success"),
        ("Pattern 7", "e4b/EN\nlunar / nameless", "Invented activities!\n'Punctuation Pass'…",
         COLOR_PRIMARY, "Discovery"),
    ]

    n = len(patterns)
    spacing = 12 / (n + 1)
    for i, (name, setup, finding, color, label) in enumerate(patterns):
        x = (i + 1) * spacing
        # Pattern node
        circle = patches.Circle((x, 3.6), 0.45,
                                facecolor=color, edgecolor="white", linewidth=2)
        ax.add_patch(circle)
        ax.text(x, 3.6, str(i + 1), ha="center", va="center",
                fontsize=14, fontweight="bold", color="white")
        # Pattern name
        ax.text(x, 4.4, name, ha="center", fontsize=9.5,
                fontweight="bold", color=COLOR_TEXT)
        # Setup
        ax.text(x, 2.8, setup, ha="center", fontsize=7.5,
                color=COLOR_MUTED)
        # Finding
        ax.text(x, 1.9, finding, ha="center", fontsize=8,
                color=COLOR_TEXT)
        # Status label
        ax.text(x, 0.9, label, ha="center", fontsize=8.5,
                fontweight="bold", color=color)

    # Connecting line
    ax.plot([spacing - 0.3, n * spacing + 0.3], [3.6, 3.6],
            color=COLOR_MUTED, linewidth=1.5, alpha=0.4, zorder=0)

    ax.text(6, 5.5, "7 Patterns — From Failure to Discovery",
            ha="center", fontsize=14, fontweight="bold", color=COLOR_TEXT)
    ax.text(6, 5.05, "Each pattern systematically modified one variable",
            ha="center", fontsize=10, color=COLOR_MUTED, style="italic")

    plt.tight_layout()
    out = FIG / "02_pattern_timeline.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=COLOR_BG)
    plt.close()
    print(f"[OK] {out}")


# =============================================================
# Figure 3: Pattern 6 vs 7 keyword comparison (the key finding)
# =============================================================
def fig_p6_vs_p7():
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.patch.set_facecolor(COLOR_BG)
    fig.suptitle("Pattern 6 (Badminton) vs Pattern 7 (Lunar / Name-less)",
                 fontsize=14, fontweight="bold", color=COLOR_TEXT, y=0.98)

    # --- Subplot 1: Existing badminton terms ---
    ax = axes[0, 0]
    ax.set_facecolor(COLOR_BG)
    terms = ["court", "shuttle", "racket", "doubles", "singles", "badminton"]
    p6 = [1926, 993, 225, 165, 198, 221]
    p7 = [0, 0, 0, 0, 0, 0]
    x = np.arange(len(terms))
    w = 0.35
    ax.bar(x - w / 2, p6, w, label="Pattern 6", color=COLOR_ACCENT)
    ax.bar(x + w / 2, p7, w, label="Pattern 7", color=COLOR_PRIMARY)
    ax.set_xticks(x)
    ax.set_xticklabels(terms, rotation=30, ha="right", fontsize=9)
    ax.set_title("Badminton-specific terms (P7 = 0)",
                 fontsize=11, fontweight="bold")
    ax.set_ylabel("# mentions")
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- Subplot 2: Lunar / artificial life terms ---
    ax = axes[0, 1]
    ax.set_facecolor(COLOR_BG)
    terms = ["lunar", "habitat", "moon", "lifeform", "artificial life"]
    p6 = [0, 0, 0, 0, 0]
    p7 = [93, 128, 41, 53, 35]
    x = np.arange(len(terms))
    ax.bar(x - w / 2, p6, w, label="Pattern 6", color=COLOR_ACCENT)
    ax.bar(x + w / 2, p7, w, label="Pattern 7", color=COLOR_PRIMARY)
    ax.set_xticks(x)
    ax.set_xticklabels(terms, rotation=30, ha="right", fontsize=9)
    ax.set_title("Lunar / artificial life terms (P6 = 0)",
                 fontsize=11, fontweight="bold")
    ax.set_ylabel("# mentions")
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- Subplot 3: Invented concepts in P7 ---
    ax = axes[1, 0]
    ax.set_facecolor(COLOR_BG)
    concepts = ["Punctuation\nPass", "Pass-Circle\n-Pass", "Silent\nTransfer",
                "Shape-Pass", "Light-Led"]
    counts = [413, 309, 196, 168, 150]
    bars = ax.barh(concepts, counts, color=COLOR_HIGHLIGHT)
    ax.set_title("Invented concepts (Pattern 7)",
                 fontsize=11, fontweight="bold")
    ax.set_xlabel("# mentions")
    for bar, c in zip(bars, counts):
        ax.text(c + 8, bar.get_y() + bar.get_height() / 2,
                str(c), va="center", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- Subplot 4: Creative concepts P6 vs P7 ---
    ax = axes[1, 1]
    ax.set_facecolor(COLOR_BG)
    terms = ["rhythm", "rule", "watch", "gentle", "flow", "fan"]
    p6 = [899, 233, 153, 601, 1341, 254]
    p7 = [10371, 2536, 1557, 5612, 7749, 813]
    x = np.arange(len(terms))
    ax.bar(x - w / 2, p6, w, label="Pattern 6", color=COLOR_ACCENT)
    ax.bar(x + w / 2, p7, w, label="Pattern 7", color=COLOR_PRIMARY)
    ax.set_xticks(x)
    ax.set_xticklabels(terms, rotation=30, ha="right", fontsize=9)
    ax.set_title("Creative concepts (P7 amplified)",
                 fontsize=11, fontweight="bold")
    ax.set_ylabel("# mentions")
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out = FIG / "03_p6_vs_p7.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=COLOR_BG)
    plt.close()
    print(f"[OK] {out}")


# =============================================================
# Figure 4: Phase progression (Period 1 → 2 → 3) Pattern 5
# =============================================================
def fig_phase_progression():
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)

    # Period split (from Pattern 5 analysis)
    periods = ["Period 1\n(Steps 1-26)\n'Initial exploration'",
               "Period 2\n(Steps 27-53)\n'Group formation'",
               "Period 3\n(Steps 54-80)\n'Mature dynamics'"]
    play_pct = [77.1, 69.4, 63.7]
    game_pct = [66.3, 52.2, 44.7]
    sport_pct = [12.3, 31.3, 20.9]

    x = np.arange(len(periods))
    w = 0.27
    ax.bar(x - w, play_pct, w, label="Play (free, casual)",
           color=COLOR_PRIMARY, alpha=0.85)
    ax.bar(x, game_pct, w, label="Game (rules, drills)",
           color=COLOR_ACCENT, alpha=0.85)
    ax.bar(x + w, sport_pct, w, label="Sport (competition, perform)",
           color=COLOR_HIGHLIGHT, alpha=0.95)

    for i, vals in enumerate(zip(play_pct, game_pct, sport_pct)):
        for j, v in enumerate(vals):
            ax.text(i + (j - 1) * w, v + 1.5, f"{v:.0f}%",
                    ha="center", fontsize=9, color=COLOR_TEXT)

    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=10)
    ax.set_ylabel("% of messages with phase keywords")
    ax.set_title("Caillois progression: Play → Game → Sport (Pattern 5)",
                 fontsize=13, fontweight="bold", color=COLOR_TEXT)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.2, axis="y")

    plt.tight_layout()
    out = FIG / "04_phase_progression.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=COLOR_BG)
    plt.close()
    print(f"[OK] {out}")


# =============================================================
# Figure 5: Persona archetypes
# =============================================================
def fig_personas():
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)
    ax.axis("off")

    archetypes = [
        ("Competitive", 4, "Win-driven, intense", COLOR_DANGER),
        ("Disciplined", 4, "Drill-focused, methodical", "#0284c7"),
        ("Analytical",  3, "Pattern-watching, strategic", COLOR_PRIMARY),
        ("Supportive",  3, "Cheer, encourage", COLOR_HIGHLIGHT),
        ("Social",      3, "Connect, organize", "#16a34a"),
        ("Casual",      3, "Easy-going, fun-first", COLOR_MUTED),
    ]

    n = len(archetypes)
    box_w, box_h = 1.6, 1.5
    spacing = 1.85
    total_w = (n - 1) * spacing
    start_x = (12 - total_w) / 2

    for i, (name, count, desc, color) in enumerate(archetypes):
        x = start_x + i * spacing
        rect = FancyBboxPatch(
            (x - box_w / 2, 1.5), box_w, box_h,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            linewidth=2, edgecolor=color, facecolor="white",
        )
        ax.add_patch(rect)
        ax.text(x, 2.6, name, ha="center", fontsize=10,
                fontweight="bold", color=color)
        ax.text(x, 2.25, f"{count} agents",
                ha="center", fontsize=10, color=COLOR_MUTED)
        ax.text(x, 1.85, desc, ha="center", fontsize=8.5,
                color=COLOR_TEXT, style="italic")

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.text(6, 3.8, "20 Agents · 6 Persona Archetypes",
            ha="center", fontsize=14, fontweight="bold", color=COLOR_TEXT)
    ax.text(6, 3.4, "Gender balance enforced: 10 male / 10 female",
            ha="center", fontsize=10, color=COLOR_MUTED, style="italic")
    ax.text(6, 0.7,
            "Each persona shapes how an agent plays, watches, talks, "
            "and coordinates — driving emergent role differentiation.",
            ha="center", fontsize=10, color=COLOR_MUTED)

    plt.tight_layout()
    out = FIG / "05_personas.png"
    plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=COLOR_BG)
    plt.close()
    print(f"[OK] {out}")


if __name__ == "__main__":
    print("Generating figures for the submission PDF...")
    fig_system_diagram()
    fig_pattern_timeline()
    fig_p6_vs_p7()
    fig_phase_progression()
    fig_personas()
    print("\nAll figures saved to:", FIG)
