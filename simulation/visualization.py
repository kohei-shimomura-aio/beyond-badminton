"""
Visualization for LLM Multi-Agent 2D Simulation
"""
import matplotlib
import os
import time
import logging
from typing import List, Dict, Tuple, Optional

# Set backend for compatibility (Mac, Linux, WSL)
GUI_BACKENDS = ['TkAgg', 'Qt5Agg', 'MacOSX', 'Qt4Agg']
NON_GUI_BACKENDS = ['agg', 'pdf', 'svg', 'ps']

# Visualization constants
FIGURE_SIZE = (11, 11)
STATS_FIGURE_SIZE = (12, 8)
DPI = 150
INITIAL_WINDOW_DELAY = 0.5
VISUALIZATION_PAUSE = 0.05
STATS_PAUSE = 0.1

# Agent visualization constants
AGENT_SIZE_IN_BAR = 450    # Star marker inside a court (slightly larger for ID visibility)
AGENT_SIZE_OUTSIDE = 320   # Circle marker outside (big enough to fit ID inside)
AGENT_ALPHA = 0.92
AGENT_EDGE_LINEWIDTH = 1.6
COMMUNICATION_LINK_ALPHA = 0.4

# Gender colors (vivid, high contrast on light background)
COLOR_MALE = '#2563eb'     # Blue
COLOR_FEMALE = '#ec4899'   # Pink

# Place visualization constants
BAR_LINEWIDTH = 2.5
BAR_ALPHA = 0.45
NET_COLOR = '#334155'
NET_LINEWIDTH = 2.5

# Distinct per-room color overrides (fallback to place_type_colors if not listed)
ROOM_COLORS = {
    'room_a': '#bae6fd',
    'room_b': '#bbf7d0',
    'court_a': '#bae6fd',
    'court_b': '#bbf7d0',
    'arena':  '#cbd5e1',   # Lunar / neutral grey for Pattern 7 arena
}

# Fire / Pressure drop zone visualization constants
FIRE_MARKER_SIZE = 260
FIRE_CIRCLE_ALPHA = 0.18
FIRE_CIRCLE_LINEWIDTH = 2.5

# Phase definition (aligned with config.yaml pressure drop start_steps)
PHASE_A_END = 40    # Steps 1-40: both rooms open
PHASE_B_END = 80    # Steps 41-80: room A pressure drop
# Steps 81+: both rooms pressure drop (Phase C)


# ===========================================================
# Theme system — applied automatically based on place type
# ===========================================================
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

THEME_LUNAR = {
    'name':         'lunar',
    'fig_bg':       '#0a0e27',
    'ax_bg':        '#0f1a3a',
    'spine':        '#1e2a52',
    'grid':         '#1e2a52',
    'grid_alpha':   0.10,
    'axis_label':   '#94a3b8',
    'tick':         '#475569',
    'title_color':  '#e0e7ff',
    'subtitle_color':'#94a3b8',
    'phase_text':   '#e0e7ff',
    'line_color':   '#cbd5e1',     # silver — visible on dark bg
    'corner_dot':   '#60a5fa',
    'comm_color':   '#a78bfa',
    'agent_edge':   '#f1f5f9',
    'agent_label':  '#f1f5f9',
    'legend_face':  '#0a0e27',
    'legend_text':  '#f1f5f9',
    'arena_fill':   '#60a5fa',     # cyan tint inside arena
    'arena_fill_alpha': 0.16,      # slightly stronger so arena floor is clearly demarcated
    'bg_image':     os.path.join(ASSETS_DIR, 'bg_lunar2.png'),
    'zoom':         1.25,
    'darken':       0.18,
    'is_dark':      True,
}

THEME_BADMINTON = {
    'name':         'badminton',
    'fig_bg':       '#0d1f17',
    'ax_bg':        '#1a3a2e',
    'spine':        '#2d5a40',
    'grid':         '#2d5a40',
    'grid_alpha':   0.10,
    'axis_label':   '#cbd5e1',
    'tick':         '#94a3b8',
    'title_color':  '#fef3c7',
    'subtitle_color':'#cbd5e1',
    'phase_text':   '#fef3c7',
    'line_color':   '#fef3c7',     # cream — visible on dark green bg
    'corner_dot':   '#fbbf24',
    'comm_color':   '#fbbf24',
    'agent_edge':   '#f1f5f9',
    'agent_label':  '#f1f5f9',
    'legend_face':  '#1a3a2e',
    'legend_text':  '#f1f5f9',
    'arena_fill':   '#bae6fd',     # subtle court-blue tint
    'arena_fill_alpha': 0.08,      # keep court fill subtle (markings already pop)
    'bg_image':     os.path.join(ASSETS_DIR, 'bg_badminton.png'),
    'zoom':         1.0,
    'darken':       0.18,
    'is_dark':      True,
}

THEME_DEFAULT = {
    'name':         'default',
    'fig_bg':       '#f8fafc',
    'ax_bg':        '#ffffff',
    'spine':        '#cbd5e1',
    'grid':         '#94a3b8',
    'grid_alpha':   0.18,
    'axis_label':   '#94a3b8',
    'tick':         '#94a3b8',
    'title_color':  '#1e293b',
    'subtitle_color':'#475569',
    'phase_text':   '#1e293b',
    'line_color':   '#0f172a',
    'corner_dot':   '#2563eb',
    'comm_color':   '#6366f1',
    'agent_edge':   'white',
    'agent_label':  'white',
    'legend_face':  'white',
    'legend_text':  '#1e293b',
    'bg_image':     None,
    'zoom':         1.0,
    'darken':       0.0,
    'is_dark':      False,
}


def _detect_theme(places: List[Dict]) -> Dict:
    """Pick the theme based on the first place's type. Falls back to default."""
    if not places:
        return THEME_DEFAULT
    place_type = places[0].get('type', '').lower()
    if place_type == 'rectangular_arena':
        return THEME_LUNAR
    if place_type == 'badminton_court':
        return THEME_BADMINTON
    return THEME_DEFAULT

# Set backend for compatibility (Mac, Linux, WSL)
backend_set = False

# Check if we're in WSL or headless environment
is_wsl = 'microsoft' in os.uname().release.lower() if hasattr(os, 'uname') else False
is_headless = not os.environ.get('DISPLAY') and not is_wsl

if is_wsl or is_headless:
    try:
        matplotlib.use('Agg')
        backend_set = True
        import logging
        logger = logging.getLogger(__name__)
        logger.info("Using Agg backend (non-GUI) for WSL/headless environment")
    except Exception:
        pass
else:
    for backend_name in GUI_BACKENDS:
        try:
            matplotlib.use(backend_name)
            backend_set = True
            break
        except (ImportError, ValueError):
            continue

if not backend_set:
    try:
        matplotlib.use('Agg')
        backend_set = True
        import logging
        logger = logging.getLogger(__name__)
        logger.warning("No GUI backend available. Using Agg backend (non-GUI). Visualization windows will not display.")
    except Exception:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("Failed to set matplotlib backend. Visualization may not work.")

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
from utils import get_place_half_sizes

logger = logging.getLogger(__name__)


class Visualizer:
    """Visualization class for simulation"""

    def __init__(self, half_space_size: int, places: List[Dict], num_agents: int = None):
        self.half_space_size = half_space_size
        self.places = places
        self.num_agents = num_agents
        self.fig = None
        self.ax = None
        self.figure_initialized = False
        self.theme = _detect_theme(places)
        self._bg_array = self._load_bg_image()

    def _load_bg_image(self):
        """Load + crop the theme's background image once. Returns None if not available."""
        bg_path = self.theme.get('bg_image')
        if not bg_path or not os.path.exists(bg_path):
            return None
        try:
            from PIL import Image
            img = Image.open(bg_path).convert('RGB')
            arr = np.asarray(img) / 255.0
            zoom = float(self.theme.get('zoom', 1.0))
            if zoom > 1.0:
                h, w, _ = arr.shape
                new_h = int(h / zoom)
                new_w = int(w / zoom)
                y0 = (h - new_h) // 2
                x0 = (w - new_w) // 2
                arr = arr[y0:y0 + new_h, x0:x0 + new_w]
            darken = float(self.theme.get('darken', 0.0))
            if darken > 0:
                arr = arr * (1 - darken)
            return arr
        except Exception as e:
            logger.warning(f"Failed to load bg image {bg_path}: {e}")
            return None

    def setup_figure(self, reuse_existing: bool = False):
        """Setup matplotlib figure with theme-aware aesthetic."""
        if reuse_existing and self.fig is not None:
            self.ax.clear()
        else:
            self.fig, self.ax = plt.subplots(figsize=FIGURE_SIZE)
            self.figure_initialized = True

        theme = self.theme
        self.fig.patch.set_facecolor(theme['fig_bg'])
        self.ax.set_facecolor(theme['ax_bg'])

        self.ax.set_xlim(-self.half_space_size, self.half_space_size)
        self.ax.set_ylim(-self.half_space_size, self.half_space_size)
        self.ax.set_aspect('equal')

        # Display background image if available (zorder 0, behind everything)
        if self._bg_array is not None:
            self.ax.imshow(
                self._bg_array,
                extent=(-self.half_space_size, self.half_space_size,
                        -self.half_space_size, self.half_space_size),
                origin='upper',
                zorder=0,
                interpolation='bilinear',
            )

        for spine in ('top', 'right', 'left', 'bottom'):
            self.ax.spines[spine].set_color(theme['spine'])
            self.ax.spines[spine].set_linewidth(0.8)
        self.ax.tick_params(colors=theme['tick'], labelsize=10)
        self.ax.set_xlabel('X', color=theme['axis_label'], fontsize=11)
        self.ax.set_ylabel('Y', color=theme['axis_label'], fontsize=11)
        self.ax.grid(True, alpha=theme['grid_alpha'], linestyle='--',
                     color=theme['grid'], zorder=0.5)

    def draw_bars(self, place_status: Optional[Dict] = None):
        """Draw all place areas (badminton courts, bars, cafes, etc.).

        Supports both square places (`half_size`) and rectangular places
        (`half_size_x` + `half_size_y`). For rectangular badminton courts
        with the long axis on Y (taller than wide), draws realistic court
        markings: net, front service lines, center line, singles boundary,
        back service lines.
        """
        place_type_colors = {
            'bar': 'lightblue',
            'cafe': 'lightcoral',
            'library': 'lightgreen',
            'restaurant': 'lightyellow',
            'park': 'lightpink',
            'badminton_court': '#bae6fd',
            'rectangular_arena': '#cbd5e1',   # Neutral lunar tone
        }
        default_colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightpink']

        for i, place in enumerate(self.places):
            half_size_x, half_size_y = get_place_half_sizes(place)
            center_x = place['center_x']
            center_y = place['center_y']
            if 'name' not in place:
                raise ValueError(f"Place at index {i} is missing required field: 'name'")
            place_name = place['name']
            place_type = place['type']
            capacity = place.get('capacity', 0)

            # Color resolution
            if place_name in ROOM_COLORS:
                face_color = ROOM_COLORS[place_name]
                edge_color = '#0284c7' if place_name.endswith('_a') else '#16a34a'
            elif place_type in place_type_colors:
                face_color = place_type_colors[place_type]
                edge_color = '#1e40af'
            else:
                face_color = default_colors[i % len(default_colors)]
                edge_color = '#1e40af'

            place_width = 2 * half_size_x + 1
            place_height = 2 * half_size_y + 1
            x0_rect = center_x - half_size_x - 0.5
            y0_rect = center_y - half_size_y - 0.5

            # On dark themes (lunar / badminton with bg image), override the
            # face/edge colors so they don't clash with the photo background.
            if self.theme.get('is_dark'):
                place_face = self.theme.get('arena_fill', self.theme['line_color'])
                place_face_alpha = self.theme.get('arena_fill_alpha', 0.06)
                place_edge = self.theme['line_color']
                # Subtle shadow band beneath the place to ground it on the bg
                shadow_rect = patches.Rectangle(
                    (x0_rect - 0.05, y0_rect - 0.18),
                    place_width + 0.10, 0.18,
                    linewidth=0,
                    facecolor='#000000',
                    alpha=0.30,
                    zorder=0.8,
                )
                self.ax.add_patch(shadow_rect)
            else:
                place_face = face_color
                place_face_alpha = BAR_ALPHA
                place_edge = edge_color

            place_rect = patches.Rectangle(
                (x0_rect, y0_rect),
                place_width, place_height,
                linewidth=BAR_LINEWIDTH,
                edgecolor=place_edge,
                facecolor=place_face,
                alpha=place_face_alpha,
                label=f"{place_name}",
                zorder=1,
            )
            self.ax.add_patch(place_rect)

            # On dark themes, add corner LED dots for grounded look
            if self.theme.get('is_dark'):
                for cx_dot, cy_dot in [(x0_rect, y0_rect),
                                       (x0_rect + place_width, y0_rect),
                                       (x0_rect, y0_rect + place_height),
                                       (x0_rect + place_width, y0_rect + place_height)]:
                    self.ax.scatter(cx_dot, cy_dot, s=24,
                                    c=self.theme['corner_dot'],
                                    alpha=0.9, zorder=4, edgecolors='none')

            # ----- Generic vertical barrier for rectangular_arena type -----
            # Pattern 7: name-less arena. Just draw the central barrier (no service lines).
            if place_type == 'rectangular_arena' and half_size_y > half_size_x:
                line_color = self.theme['line_color']
                self.ax.plot(
                    [center_x - half_size_x - 0.5, center_x + half_size_x + 0.5],
                    [center_y, center_y],
                    color=line_color,
                    linewidth=2.6,
                    alpha=0.95,
                    zorder=2.2,
                )
                self.ax.text(
                    center_x + half_size_x + 0.6, center_y, 'BARRIER',
                    fontsize=7,
                    ha='left', va='center',
                    color=line_color,
                    fontweight='bold',
                    alpha=0.7,
                    zorder=3,
                )

            # ----- Realistic badminton court markings -----
            # Drawn for rectangular badminton_court places where long axis = Y.
            if place_type == 'badminton_court' and half_size_y > half_size_x:
                line_color = self.theme['line_color']

                # Net (across the full X width, at Y = center_y)
                self.ax.plot(
                    [center_x - half_size_x - 0.5, center_x + half_size_x + 0.5],
                    [center_y, center_y],
                    color=line_color,
                    linewidth=2.6,
                    alpha=0.9,
                    zorder=2.2,
                )
                # NET label
                self.ax.text(
                    center_x + half_size_x + 0.6, center_y, 'NET',
                    fontsize=7,
                    ha='left', va='center',
                    color=line_color,
                    fontweight='bold',
                    alpha=0.75,
                    zorder=3,
                )

                # Front service lines (parallel to net, ±1 unit from net)
                for offset in (-1, 1):
                    self.ax.plot(
                        [center_x - half_size_x - 0.5, center_x + half_size_x + 0.5],
                        [center_y + offset, center_y + offset],
                        color=line_color,
                        linewidth=0.9,
                        alpha=0.55,
                        zorder=2,
                    )

                # Center line (perpendicular to net, full Y span of court)
                self.ax.plot(
                    [center_x, center_x],
                    [center_y - half_size_y - 0.5, center_y + half_size_y + 0.5],
                    color=line_color,
                    linewidth=0.9,
                    alpha=0.55,
                    zorder=2,
                )

                # Singles side-line (inset on the X / wide sides)
                singles_inset = 0.35
                singles_rect = patches.Rectangle(
                    (center_x - half_size_x - 0.5 + singles_inset,
                     center_y - half_size_y - 0.5),
                    place_width - 2 * singles_inset,
                    place_height,
                    linewidth=0.9,
                    edgecolor=line_color,
                    facecolor='none',
                    alpha=0.55,
                    linestyle='-',
                    zorder=2,
                )
                self.ax.add_patch(singles_rect)

                # Back service lines for doubles (inset from back boundary)
                back_doubles_inset = 0.5
                for back_y in (
                    center_y - half_size_y - 0.5 + back_doubles_inset,
                    center_y + half_size_y + 0.5 - back_doubles_inset,
                ):
                    self.ax.plot(
                        [center_x - half_size_x - 0.5 + singles_inset,
                         center_x + half_size_x + 0.5 - singles_inset],
                        [back_y, back_y],
                        color=line_color,
                        linewidth=0.7,
                        alpha=0.4,
                        zorder=2,
                    )

            # Theme-aware label colors
            if self.theme.get('is_dark'):
                label_color = self.theme['line_color']
                badge_face = self.theme['corner_dot']
                badge_text_color = '#0a0e27' if self.theme['name'] == 'lunar' else '#0d1f17'
            else:
                label_color = edge_color
                badge_face = edge_color
                badge_text_color = 'white'

            # Big court letter label (A or B) — offset to upper half if rectangular
            letter = None
            if place_name.lower().endswith('_a'):
                letter = 'A'
            elif place_name.lower().endswith('_b'):
                letter = 'B'
            if letter:
                if place_type == 'badminton_court' and half_size_y > half_size_x:
                    # On rectangular court: place letter in upper half (above net)
                    letter_y = center_y + half_size_y * 0.55
                    letter_size = 38
                else:
                    letter_y = center_y
                    letter_size = 78
                self.ax.text(
                    center_x, letter_y,
                    letter,
                    fontsize=letter_size,
                    ha='center', va='center',
                    color=label_color,
                    fontweight='bold',
                    alpha=0.22,
                    zorder=1.5,
                )

            # Place name label (above the court, top-left)
            self.ax.text(
                center_x - half_size_x - 0.3, center_y + half_size_y + 0.4,
                place_name,
                fontsize=11,
                ha='left', va='bottom',
                color=label_color,
                fontweight='bold',
                zorder=4,
            )

            # Capacity badge (above the court, top-right)
            if place_status and 'places' in place_status and place_name in place_status['places']:
                agents_here = place_status['places'][place_name]['agents_in_place']
                badge_text = f"{agents_here}/{capacity}"
            else:
                badge_text = f"cap {capacity}"
            self.ax.text(
                center_x + half_size_x + 0.3, center_y + half_size_y + 0.4,
                badge_text,
                fontsize=11,
                ha='right', va='bottom',
                color=badge_text_color,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.35', facecolor=badge_face, alpha=0.92, edgecolor='none'),
                zorder=4,
            )

    def draw_fires(self, fire_states: List[Dict]):
        """Draw pressure drop zones: center markers + perception radius circles."""
        fire_cmap = matplotlib.colormaps['YlOrRd']

        for fire in fire_states:
            if not fire.get('active'):
                continue

            fx, fy = fire['position']
            radius = fire['radius']
            intensity = fire['intensity']
            name = fire.get('name', 'zone')

            face_color = fire_cmap(min(intensity + 0.15, 1.0))

            fire_circle = patches.Circle(
                (fx, fy),
                radius,
                linewidth=FIRE_CIRCLE_LINEWIDTH,
                edgecolor='#dc2626',
                facecolor=face_color,
                alpha=FIRE_CIRCLE_ALPHA + 0.12,
                linestyle='--',
                zorder=5,
            )
            self.ax.add_patch(fire_circle)

            self.ax.scatter(
                fx, fy,
                c='#dc2626',
                s=FIRE_MARKER_SIZE,
                marker='v',
                edgecolors='#7f1d1d',
                linewidths=2,
                zorder=11,
            )
            self.ax.text(
                fx, fy, '!',
                fontsize=18,
                ha='center', va='center',
                color='white',
                fontweight='bold',
                zorder=12,
            )

            self.ax.text(
                fx, fy - 2.0,
                f'PRESSURE DROP\n{name}  (intensity {intensity})',
                fontsize=10.5,
                ha='center', va='top',
                color='#7f1d1d',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.88, edgecolor='#dc2626'),
                zorder=11,
            )

    def draw_agents(
        self,
        agents: List,
        agents_by_place: Dict[str, List[int]],
        communication_links: List[Tuple[int, int]] = None
    ):
        """Draw agents and communication links"""
        comm_color = self.theme.get('comm_color', '#6366f1')
        agent_edge = self.theme.get('agent_edge', 'white')
        agent_label = self.theme.get('agent_label', 'white')
        if communication_links:
            for agent_id1, agent_id2 in communication_links:
                agent1 = agents[agent_id1]
                agent2 = agents[agent_id2]
                self.ax.plot(
                    [agent1.position[0], agent2.position[0]],
                    [agent1.position[1], agent2.position[1]],
                    color=comm_color,
                    alpha=COMMUNICATION_LINK_ALPHA + 0.15,
                    linewidth=1.3,
                    zorder=6,
                )

        for agent in agents:
            color = COLOR_MALE if agent.gender == 'male' else COLOR_FEMALE
            if agent.in_place and agent.current_place:
                marker = '*'
                size = AGENT_SIZE_IN_BAR
            else:
                marker = 'o'
                size = AGENT_SIZE_OUTSIDE

            # Soft outer halo for better visibility on dark backgrounds
            if self.theme.get('is_dark') and marker == 'o':
                self.ax.scatter(
                    agent.position[0],
                    agent.position[1],
                    c=color,
                    s=size + 200,
                    marker='o',
                    alpha=0.18,
                    edgecolors='none',
                    zorder=7.5,
                )

            self.ax.scatter(
                agent.position[0],
                agent.position[1],
                c=color,
                s=size,
                marker=marker,
                alpha=AGENT_ALPHA,
                edgecolors=agent_edge,
                linewidths=AGENT_EDGE_LINEWIDTH,
                zorder=8,
            )

            # For stars: solid disk underneath the ID for readability
            if marker == '*':
                self.ax.scatter(
                    agent.position[0],
                    agent.position[1],
                    c=color,
                    s=140,
                    marker='o',
                    alpha=1.0,
                    edgecolors='none',
                    zorder=8.5,
                )

            id_fontsize = 10 if marker == '*' else 10
            self.ax.text(
                agent.position[0], agent.position[1],
                str(agent.id),
                fontsize=id_fontsize,
                ha='center', va='center',
                color=agent_label,
                fontweight='bold',
                zorder=9,
            )

    def visualize_step(
        self,
        agents: List,
        place_status: Dict,
        step: int,
        communication_radius: float = None,
        save_path: str = None,
        fire_states: Optional[List[Dict]] = None
    ):
        """Visualize a single simulation step"""
        reuse = save_path is None and self.figure_initialized
        self.setup_figure(reuse_existing=reuse)
        self.draw_bars(place_status=place_status)
        self.draw_fires(fire_states or [])

        # Get agents by place
        agents_by_place = {}
        for place in self.places:
            agents_by_place[place['name']] = [agent.id for agent in agents
                                          if agent.in_place and agent.current_place == place['name']]

        # Find communication links (same-area condition: same place or both outside)
        communication_links = []
        if communication_radius:
            for i, agent1 in enumerate(agents):
                for agent2 in agents[i+1:]:
                    dist = agent1.distance_to(agent2.position)
                    same_area = (
                        (not agent1.in_place and not agent2.in_place) or
                        (agent1.in_place and agent2.in_place and
                         agent1.current_place == agent2.current_place)
                    )
                    if dist <= communication_radius and same_area:
                        communication_links.append((agent1.id, agent2.id))

        self.draw_agents(agents, agents_by_place, communication_links)

        # ===== Build two-line title with phase indicator =====
        active_fires_for_label = [f for f in (fire_states or []) if f.get('active')]
        any_fire_configured = bool(active_fires_for_label)
        if any_fire_configured:
            if step <= PHASE_A_END:
                phase_label = 'Phase A'
                phase_desc = 'Both rooms open'
                phase_color = '#6366f1'
            elif step <= PHASE_B_END:
                phase_label = 'Phase B'
                phase_desc = 'Room A: pressure drop'
                phase_color = '#f97316'
            else:
                phase_label = 'Phase C'
                phase_desc = 'Both rooms unusable'
                phase_color = '#dc2626'
        else:
            # Time-based phases (aligned with announcements at step 34 and 67)
            if step <= 33:
                phase_label = 'Phase I'
                phase_desc = 'Initial exploration'
                phase_color = '#6366f1'
            elif step <= 66:
                phase_label = 'Phase II'
                phase_desc = 'Recreational session'
                phase_color = '#10b981'
            else:
                phase_label = 'Phase III'
                phase_desc = 'Memory crystallisation'
                phase_color = '#8b5cf6'

        # Per-place stats line
        place_stats_parts = []
        if 'places' in place_status:
            for place_name, status in place_status['places'].items():
                place_stats_parts.append(
                    f"{place_name} {status['agents_in_place']}/{status['capacity']}"
                )
        outside_count = len(agents) - place_status.get('agents_in_place', 0)
        place_stats_parts.append(f"outside {outside_count}")

        active_fires = [f for f in (fire_states or []) if f.get('active')]
        if active_fires:
            agents_in_any_fire = set()
            for fire in active_fires:
                for a in agents:
                    if a.distance_to(fire['position']) <= fire['radius']:
                        agents_in_any_fire.add(a.id)
            place_stats_parts.append(f"⚠ in zone: {len(agents_in_any_fire)}")

        stats_line = '  ·  '.join(place_stats_parts)

        # Theme-aware text colors
        title_col = self.theme.get('title_color', phase_color)
        subtitle_col = self.theme.get('subtitle_color', '#475569')
        stats_col = self.theme.get('subtitle_color', '#334155')
        legend_face = self.theme.get('legend_face', '#ffffff')
        legend_text = self.theme.get('legend_text', '#1e293b')
        legend_edge = self.theme.get('spine', '#cbd5e1')
        agent_edge_legend = self.theme.get('agent_edge', 'white')

        # Apply phase color override only on light theme; on dark themes use
        # theme's title color for consistent palette
        title_color_actual = phase_color if not self.theme.get('is_dark') else title_col

        self.fig.suptitle('')
        self.ax.set_title('')
        self.fig.text(
            0.5, 0.970,
            f"{phase_label}  —  Step {step}",
            ha='center', va='top',
            fontsize=20, fontweight='bold', color=title_color_actual,
        )
        self.fig.text(
            0.5, 0.935,
            phase_desc,
            ha='center', va='top',
            fontsize=12, color=subtitle_col, style='italic',
        )
        self.fig.text(
            0.5, 0.907,
            stats_line,
            ha='center', va='top',
            fontsize=11, color=stats_col, family='monospace',
        )

        # ===== Compact legend (lower-left) =====
        from matplotlib.lines import Line2D
        comm_color_for_legend = self.theme.get('comm_color', '#6366f1')
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=COLOR_MALE,
                   markeredgecolor=agent_edge_legend, markersize=11, label='Male (off court)'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=COLOR_FEMALE,
                   markeredgecolor=agent_edge_legend, markersize=11, label='Female (off court)'),
            Line2D([0], [0], marker='*', color='w', markerfacecolor=COLOR_MALE,
                   markeredgecolor=agent_edge_legend, markersize=16, label='Male (on court)'),
            Line2D([0], [0], marker='*', color='w', markerfacecolor=COLOR_FEMALE,
                   markeredgecolor=agent_edge_legend, markersize=16, label='Female (on court)'),
            Line2D([0], [0], color=comm_color_for_legend,
                   linewidth=1.8, alpha=0.7, label='Communication'),
        ]
        if active_fires:
            legend_elements.append(
                Line2D([0], [0], marker='v', color='w', markerfacecolor='#dc2626',
                       markeredgecolor='#7f1d1d', markersize=13,
                       label='Pressure drop source')
            )
            legend_elements.append(
                Line2D([0], [0], color='#dc2626', linestyle='--', linewidth=1.8,
                       alpha=0.8, label='Perception radius')
            )
        leg = self.ax.legend(
            handles=legend_elements,
            loc='lower left',
            fontsize=10,
            framealpha=0.90,
            edgecolor=legend_edge,
            facecolor=legend_face,
            labelcolor=legend_text,
        )

        plt.tight_layout(rect=[0, 0, 1, 0.885])

        if save_path:
            plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
            plt.close(self.fig)
            self.fig = None
            self.ax = None
        else:
            self._display_interactive(step)

    def _display_interactive(self, step: int):
        """Display visualization interactively"""
        backend = matplotlib.get_backend()
        is_gui_backend = backend.lower() not in NON_GUI_BACKENDS

        if is_gui_backend:
            plt.ion()
            if not self.figure_initialized:
                plt.show(block=False)
                time.sleep(INITIAL_WINDOW_DELAY)
                logger.info(f"Created visualization window for step {step}")
                self.figure_initialized = True
            else:
                plt.draw()
                if hasattr(self.fig.canvas, 'flush_events'):
                    self.fig.canvas.flush_events()
            plt.pause(VISUALIZATION_PAUSE)
            logger.debug(f"Updated visualization for step {step}")
        else:
            plt.draw()
            logger.debug(f"Drew visualization for step {step} (non-GUI backend: {backend})")
            logger.warning("GUI backend not available. Use --save-frames to save visualization images.")

    def plot_statistics(
        self,
        stats: Dict,
        save_path: Optional[str] = None,
        occupancy_threshold: float = 0.6,
        agent_threshold: int = 12,
        fire_states: Optional[List[Dict]] = None
    ):
        """Plot simulation statistics"""
        num_places = len(self.places) if hasattr(self, 'places') else 1
        has_fire = 'agents_in_fire_radius' in stats and any(v > 0 for v in stats['agents_in_fire_radius'])
        num_plots = 2 + num_places + (1 if has_fire else 0)

        fig, axes = plt.subplots(num_plots, 1, figsize=STATS_FIGURE_SIZE)
        if num_plots == 1:
            axes = [axes]

        plot_idx = 0

        if 'place_occupancy' in stats and stats['place_occupancy']:
            steps = range(len(stats['place_occupancy']))
            axes[plot_idx].plot(steps, stats['place_occupancy'], 'b-', alpha=0.7, label='Overall Occupancy Rate')
            axes[plot_idx].set_xlabel('Step')
            axes[plot_idx].set_ylabel('Place Occupancy Rate')
            axes[plot_idx].set_title('Overall Place Occupancy Over Time')
            axes[plot_idx].legend()
            axes[plot_idx].grid(True, alpha=0.3)
            axes[plot_idx].set_ylim(0, 1)
            plot_idx += 1

        if 'agents_in_place' in stats and stats['agents_in_place']:
            steps = range(len(stats['agents_in_place']))
            axes[plot_idx].plot(steps, stats['agents_in_place'], 'g-', alpha=0.7, label='Total Agents in Places')
            axes[plot_idx].set_xlabel('Step')
            axes[plot_idx].set_ylabel('Number of Agents')
            axes[plot_idx].set_title('Total Number of Agents in Places Over Time')
            axes[plot_idx].legend()
            axes[plot_idx].grid(True, alpha=0.3)
            max_agents = max(stats['agents_in_place']) if stats['agents_in_place'] else 20
            axes[plot_idx].set_ylim(0, max(20, max_agents + 2))
            plot_idx += 1

        if 'places' in stats:
            place_colors = ['red', 'orange', 'green', 'purple', 'brown']
            for i, place in enumerate(self.places):
                place_name = place['name']
                if place_name in stats['places']:
                    place_stats = stats['places'][place_name]

                    if place_stats['occupancy']:
                        steps = range(len(place_stats['occupancy']))
                        color = place_colors[i % len(place_colors)]
                        axes[plot_idx].plot(
                            steps, place_stats['occupancy'],
                            color=color, alpha=0.7,
                            label=f'{place_name} Occupancy'
                        )

                    if place_stats['agents_in_place']:
                        steps = range(len(place_stats['agents_in_place']))
                        color = place_colors[i % len(place_colors)]
                        axes[plot_idx].plot(
                            steps, place_stats['agents_in_place'],
                            color=color, alpha=0.5, linestyle=':',
                            label=f'{place_name} Agents'
                        )

                    axes[plot_idx].set_xlabel('Step')
                    axes[plot_idx].set_ylabel('Occupancy / Agents')
                    axes[plot_idx].set_title(f'{place_name} Statistics Over Time')
                    axes[plot_idx].legend()
                    axes[plot_idx].grid(True, alpha=0.3)
                    axes[plot_idx].set_ylim(0, 1)
                    plot_idx += 1

        if has_fire:
            steps = range(len(stats['agents_in_fire_radius']))
            axes[plot_idx].plot(
                steps, stats['agents_in_fire_radius'],
                'r-', alpha=0.7, label='Agents in pressure drop zone'
            )
            if fire_states:
                for fire in fire_states:
                    if 'start_step' in fire:
                        fire_start_idx = fire['start_step'] - 1
                        fire_name = fire.get('name', 'Zone')
                        axes[plot_idx].axvline(
                            x=fire_start_idx, color='red', linestyle='--',
                            alpha=0.5, label=f'{fire_name} start'
                        )
            axes[plot_idx].set_xlabel('Step')
            axes[plot_idx].set_ylabel('Number of Agents')
            axes[plot_idx].set_title('Agents Within Pressure Drop Zone Over Time')
            axes[plot_idx].legend()
            axes[plot_idx].grid(True, alpha=0.3)
            max_fire = max(stats['agents_in_fire_radius']) if stats['agents_in_fire_radius'] else 20
            axes[plot_idx].set_ylim(0, max(20, max_fire + 2))
            plot_idx += 1

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
            plt.close(fig)
        else:
            backend = matplotlib.get_backend()
            is_gui_backend = backend.lower() not in NON_GUI_BACKENDS

            if is_gui_backend:
                plt.show(block=False)
                plt.pause(STATS_PAUSE)
            else:
                plt.draw()
                plt.close(fig)
                logger.warning("GUI backend not available. Statistics plot not displayed. Use --save-frames to save.")
