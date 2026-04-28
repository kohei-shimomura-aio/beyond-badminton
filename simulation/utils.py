"""
Shared utility functions for LLM-based agent in 2D worlds with multiple places.
"""
from typing import Tuple, Optional, List, Dict, TypedDict


class FireConfig(TypedDict, total=False):
    """Type definition for fire event configuration"""
    name: str  # Fire name (required)
    start_step: int  # Step at which fire appears (required)
    intensity: float  # Fire intensity (0.0 to 1.0) (required)
    radius: int  # Perception radius (required)
    center_x: int  # Fire position X (optional, random if omitted)
    center_y: int  # Fire position Y (optional, random if omitted)


class PlaceConfig(TypedDict, total=False):
    """Type definition for place configuration.

    A place can be defined either as:
      (a) Square: provide `half_size` (used for both X and Y)
      (b) Rectangle: provide `half_size_x` and `half_size_y` separately
    """
    name: str
    type: str
    center_x: int
    center_y: int
    half_size: int       # Optional, used for both X/Y if dimension-specific keys absent
    half_size_x: int     # Optional, takes priority over half_size for X
    half_size_y: int     # Optional, takes priority over half_size for Y
    capacity: int


def get_place_half_sizes(place: PlaceConfig) -> Tuple[int, int]:
    """Return (half_size_x, half_size_y) for a place, with fallback to half_size."""
    fallback = place.get('half_size', 0)
    hx = place.get('half_size_x', fallback)
    hy = place.get('half_size_y', fallback)
    return hx, hy


def is_position_in_place(
    position: Tuple[int, int],
    half_size: int,
    center_x: int = 0,
    center_y: int = 0,
    half_size_x: Optional[int] = None,
    half_size_y: Optional[int] = None
) -> bool:
    """
    Check if a position is inside a place area (centered at (center_x, center_y)).

    If half_size_x / half_size_y are provided, they take priority and a rectangle
    of that size is used. Otherwise the legacy `half_size` (square) applies.
    """
    hx = half_size_x if half_size_x is not None else half_size
    hy = half_size_y if half_size_y is not None else half_size
    x, y = position
    return (center_x - hx <= x <= center_x + hx and
            center_y - hy <= y <= center_y + hy)


def get_place_at_position(
    position: Tuple[int, int],
    places: List[PlaceConfig]
) -> Optional[PlaceConfig]:
    """Return the first place that contains the given position, or None."""
    for place in places:
        hx, hy = get_place_half_sizes(place)
        x, y = position
        cx, cy = place['center_x'], place['center_y']
        if cx - hx <= x <= cx + hx and cy - hy <= y <= cy + hy:
            return place
    return None
