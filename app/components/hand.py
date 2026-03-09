"""
UI components for rendering player hands and tiles.
"""

import reflex as rx
from typing import List


def render_tile_clickable(tile_str: str, player_idx: int) -> rx.Component:
    """
    Render a clickable mahjong tile.

    Args:
        tile_str: String representation of tile (e.g., "1m", "5p")
        player_idx: Index of the player (0-3)

    Returns:
        Reflex component for the tile
    """
    from ..state import MahjongState

    return rx.button(
        tile_str,
        on_click=lambda: MahjongState.discard_tile(player_idx, tile_str),
        padding="8px 12px",
        margin="2px",
        border="2px solid #333",
        border_radius="4px",
        background="white",
        font_size="18px",
        font_weight="bold",
        font_family="monospace",
        cursor="pointer",
        transition="all 0.2s",
        _hover={
            "background": "#e8f4f8",
            "transform": "translateY(-4px)",
        },
    )


def render_tile_static(tile_str: str) -> rx.Component:
    """
    Render a non-clickable mahjong tile.

    Args:
        tile_str: String representation of tile

    Returns:
        Reflex component for the tile
    """
    return rx.box(
        tile_str,
        padding="8px 12px",
        margin="2px",
        border="2px solid #333",
        border_radius="4px",
        background="white",
        font_size="18px",
        font_weight="bold",
        font_family="monospace",
    )


def render_hand(
    tiles: List[str],
    player_idx: int,
    player_name: str,
    is_current: bool = False,
    is_interactive: bool = False,
) -> rx.Component:
    """
    Render a player's hand.

    Args:
        tiles: List of tile strings
        player_idx: Index of the player (0-3)
        player_name: Name/position of the player
        is_current: Whether this is the current player
        is_interactive: Whether tiles are clickable

    Returns:
        Reflex component for the hand
    """
    # Use rx.cond to determine if tiles should be clickable
    tiles_display = rx.cond(
        is_interactive & is_current,
        rx.hstack(
            rx.foreach(
                tiles,
                lambda tile: render_tile_clickable(tile, player_idx)
            ),
            spacing="1",
            wrap="wrap",
        ),
        rx.hstack(
            rx.foreach(
                tiles,
                render_tile_static
            ),
            spacing="1",
            wrap="wrap",
        ),
    )

    return rx.box(
        rx.heading(
            player_name,
            size="4",
            color=rx.cond(is_current, "#2c5282", "#4a5568"),
            margin_bottom="8px",
        ),
        tiles_display,
        padding="16px",
        border_radius="8px",
        background="#f7fafc",
        border=rx.cond(is_current, "3px solid #2c5282", "1px solid #e2e8f0"),
        margin="8px",
    )


def render_melds(melds: List[dict]) -> rx.Component:
    """
    Render called melds (pon, chi, kan).

    Args:
        melds: List of meld dictionaries

    Returns:
        Reflex component for melds
    """
    if not melds:
        return rx.box()

    meld_components = []
    for meld in melds:
        meld_type = meld.get("type", "")
        tiles = meld.get("tiles", [])

        meld_box = rx.hstack(
            rx.badge(meld_type.upper(), color_scheme="green"),
            *[rx.text(tile, font_weight="bold") for tile in tiles],
            padding="4px 8px",
            border="1px solid #48bb78",
            border_radius="4px",
            margin="2px",
        )
        meld_components.append(meld_box)

    return rx.vstack(*meld_components, align_items="flex-start")
