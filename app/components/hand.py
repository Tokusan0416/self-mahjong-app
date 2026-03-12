"""
UI components for rendering player hands and tiles.
"""

import reflex as rx
from typing import List


def render_tile_clickable(tile_str: str, player_idx: int, is_drawn_tile: bool = False, size: str = "normal") -> rx.Component:
    """
    Render a clickable mahjong tile.

    Args:
        tile_str: String representation of tile (e.g., "1m", "5p")
        player_idx: Index of the player (0-3)
        is_drawn_tile: Whether this is the drawn tile (displayed on the right)
        size: Size of the tile ("normal" or "small")

    Returns:
        Reflex component for the tile
    """
    from ..state import MahjongState

    # Size configurations
    if size == "small":
        padding_val = "4px 8px"
        font_size_val = "12px"
    else:  # normal
        padding_val = "8px 12px"
        font_size_val = "18px"

    return rx.button(
        tile_str,
        on_click=lambda: MahjongState.discard_tile(player_idx, tile_str, is_drawn_tile),
        padding=padding_val,
        margin="2px",
        border="2px solid #333",
        border_radius="4px",
        background="white",
        color="#1a202c",
        font_size=font_size_val,
        font_weight="bold",
        font_family="monospace",
        cursor="pointer",
        transition="all 0.2s",
        _hover={
            "background": "#e8f4f8",
            "transform": "translateY(-4px)",
        },
    )


def render_tile_static(tile_str: str, size: str = "normal") -> rx.Component:
    """
    Render a non-clickable mahjong tile.

    Args:
        tile_str: String representation of tile
        size: Size of the tile ("normal" or "small")

    Returns:
        Reflex component for the tile
    """
    # Size configurations
    if size == "small":
        padding_val = "4px 8px"
        font_size_val = "12px"
    else:  # normal
        padding_val = "8px 12px"
        font_size_val = "18px"

    return rx.box(
        tile_str,
        padding=padding_val,
        margin="2px",
        border="2px solid #333",
        border_radius="4px",
        background="white",
        color="#1a202c",
        font_size=font_size_val,
        font_weight="bold",
        font_family="monospace",
    )


def render_hand(
    tiles: List[str],
    player_idx: int,
    player_name: str,
    is_current: bool = False,
    is_interactive: bool = False,
    can_ron: bool = False,
    can_pon: bool = False,
    can_chi: bool = False,
    can_kan: bool = False,
    last_drawn_tile: str = "",
    tile_size: str = "normal",
) -> rx.Component:
    """
    Render a player's hand.

    Args:
        tiles: List of tile strings
        player_idx: Index of the player (0-3)
        player_name: Name/position of the player
        is_current: Whether this is the current player
        is_interactive: Whether tiles are clickable
        can_ron: Whether this player can declare ron
        can_pon: Whether this player can declare pon
        can_chi: Whether this player can declare chi
        can_kan: Whether this player can declare kan
        last_drawn_tile: The most recently drawn tile (displayed separately on the right)
        tile_size: Size of tiles ("normal" or "small")

    Returns:
        Reflex component for the hand
    """
    from ..state import MahjongState

    # Create display for main hand (without last drawn tile)
    main_hand_display = rx.cond(
        is_interactive & is_current,
        rx.hstack(
            rx.foreach(
                tiles,
                lambda tile: render_tile_clickable(tile, player_idx, False, tile_size)
            ),
            spacing="1",
            wrap="wrap",
        ),
        rx.hstack(
            rx.foreach(
                tiles,
                lambda tile: render_tile_static(tile, tile_size)
            ),
            spacing="1",
            wrap="wrap",
        ),
    )

    # Create display for last drawn tile (shown separately on the right)
    drawn_tile_display = rx.cond(
        last_drawn_tile != "",
        rx.cond(
            is_interactive & is_current,
            render_tile_clickable(last_drawn_tile, player_idx, is_drawn_tile=True, size=tile_size),
            render_tile_static(last_drawn_tile, tile_size),
        ),
        rx.box(),  # Empty if no drawn tile
    )

    # Combine main hand and drawn tile with spacing
    tiles_display = rx.hstack(
        main_hand_display,
        rx.box(width="16px"),  # Spacing between main hand and drawn tile
        drawn_tile_display,
        align_items="center",
    )

    return rx.box(
        rx.heading(
            player_name,
            size="4",
            color=rx.cond(is_current, "#2c5282", "#4a5568"),
            margin_bottom="8px",
        ),
        tiles_display,
        # Call buttons (shown when available)
        rx.vstack(
            rx.cond(
                can_ron,
                rx.button(
                    "🎉 RON! (Win on Discard)",
                    on_click=lambda: MahjongState.declare_ron(player_idx),
                    color_scheme="red",
                    size="3",
                    variant="solid",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.cond(
                can_kan,
                rx.button(
                    "📦 KAN (Quad)",
                    on_click=lambda: MahjongState.declare_pon(player_idx),  # TODO: Implement declare_kan
                    color_scheme="orange",
                    size="2",
                    variant="solid",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.cond(
                can_pon,
                rx.button(
                    "🔺 PON (Triple)",
                    on_click=lambda: MahjongState.declare_pon(player_idx),
                    color_scheme="purple",
                    size="2",
                    variant="solid",
                    width="100%",
                ),
                rx.box(),
            ),
            rx.cond(
                can_chi,
                rx.button(
                    "🔄 CHI (Sequence)",
                    on_click=lambda: MahjongState.declare_chi(player_idx),
                    color_scheme="blue",
                    size="2",
                    variant="solid",
                    width="100%",
                ),
                rx.box(),
            ),
            spacing="2",
            margin_top="8px",
            width="100%",
        ),
        padding="16px",
        border_radius="8px",
        background="#f7fafc",
        border=rx.cond(is_current, "3px solid #2c5282", "1px solid #e2e8f0"),
        margin="8px",
    )


def render_melds(melds: List[str]) -> rx.Component:
    """
    Render called melds (pon, chi, kan).

    Args:
        melds: List of meld strings (e.g., "PON: 1m 1m 1m")

    Returns:
        Reflex component for melds
    """
    return rx.cond(
        melds.length() > 0,
        rx.vstack(
            rx.text("Melds:", font_weight="bold", font_size="sm", color="gray"),
            rx.foreach(
                melds,
                lambda meld_str: rx.badge(
                    meld_str,
                    color_scheme="green",
                    padding="4px 8px",
                    margin="2px",
                    font_size="sm",
                )
            ),
            align_items="flex-start",
            padding="8px",
            margin="4px",
        ),
        rx.box(),
    )
