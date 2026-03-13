"""
Mahjong table layout component - cross pattern with discards near each player.
"""

import reflex as rx
from typing import List
from .tile_image import render_tile_static_image


def render_player_discards(discards: List[str], size: str = "small") -> rx.Component:
    """
    Render a player's discard pile.

    Args:
        discards: List of discarded tiles
        size: Size of tiles

    Returns:
        Reflex component for discard pile
    """
    return rx.hstack(
        rx.foreach(
            discards,
            lambda tile: render_tile_static_image(tile, size=size),
        ),
        spacing="1",
        wrap="wrap",
        max_width="600px",
    )


def render_mahjong_table(
    # Player data
    player_hands: List[List[str]],
    player_names: List[str],
    player_discards: List[List[str]],
    player_melds: List[List[str]],
    player_last_drawn: List[str],
    current_player: int,
    # Call availability
    can_ron: List[bool],
    can_pon: List[bool],
    can_chi: List[bool],
    can_kan: List[bool],
) -> rx.Component:
    """
    Render mahjong table with cross-pattern layout.

    Layout:
        Top: Player 2 (West) with discards below
        Right: Player 1 (South) with discards to left
        Bottom: Player 0 (East) with discards above - larger display
        Left: Player 3 (North) with discards to right

    Args:
        player_hands: Hands for all players
        player_names: Names of all players
        player_discards: Discards for all players
        player_melds: Melds for all players
        player_last_drawn: Last drawn tiles for all players
        current_player: Current player index
        can_ron: Ron availability for each player
        can_pon: Pon availability for each player
        can_chi: Chi availability for each player
        can_kan: Kan availability for each player

    Returns:
        Reflex component for mahjong table
    """
    from .hand import render_hand, render_melds

    return rx.box(
        # Top player (Position 2 - West)
        rx.box(
            rx.vstack(
                render_hand(
                    player_hands[2],
                    2,
                    player_names[2],
                    is_current=current_player == 2,
                    is_interactive=True,
                    can_ron=can_ron[2],
                    can_pon=can_pon[2],
                    can_chi=can_chi[2],
                    can_kan=can_kan[2],
                    last_drawn_tile=player_last_drawn[2],
                    tile_size="small",
                ),
                render_melds(player_melds[2]),
                rx.box(
                    rx.text("Discards:", font_size="xs", font_weight="600", color="#718096", margin_bottom="4px"),
                    render_player_discards(player_discards[2], size="small"),
                    margin_top="8px",
                ),
                spacing="2",
                align="center",
            ),
            position="absolute",
            top="0",
            left="50%",
            transform="translateX(-50%)",
            width="100%",
            max_width="700px",
        ),
        # Middle row: Left, Center (empty), Right
        rx.hstack(
            # Left player (Position 3 - North)
            rx.box(
                rx.vstack(
                    render_hand(
                        player_hands[3],
                        3,
                        player_names[3],
                        is_current=current_player == 3,
                        is_interactive=True,
                        can_ron=can_ron[3],
                        can_pon=can_pon[3],
                        can_chi=can_chi[3],
                        can_kan=can_kan[3],
                        last_drawn_tile=player_last_drawn[3],
                        tile_size="small",
                    ),
                    render_melds(player_melds[3]),
                    rx.box(
                        rx.text("Discards:", font_size="xs", font_weight="600", color="#718096", margin_bottom="4px"),
                        render_player_discards(player_discards[3], size="small"),
                        margin_top="8px",
                    ),
                    spacing="2",
                    align="center",
                ),
                width="250px",
            ),
            # Center area (empty - for visual balance)
            rx.box(
                flex="1",
                min_height="200px",
            ),
            # Right player (Position 1 - South)
            rx.box(
                rx.vstack(
                    render_hand(
                        player_hands[1],
                        1,
                        player_names[1],
                        is_current=current_player == 1,
                        is_interactive=True,
                        can_ron=can_ron[1],
                        can_pon=can_pon[1],
                        can_chi=can_chi[1],
                        can_kan=can_kan[1],
                        last_drawn_tile=player_last_drawn[1],
                        tile_size="small",
                    ),
                    render_melds(player_melds[1]),
                    rx.box(
                        rx.text("Discards:", font_size="xs", font_weight="600", color="#718096", margin_bottom="4px"),
                        render_player_discards(player_discards[1], size="small"),
                        margin_top="8px",
                    ),
                    spacing="2",
                    align="center",
                ),
                width="250px",
            ),
            spacing="4",
            align="start",
            justify="between",
            width="100%",
            margin_top="140px",
            margin_bottom="20px",
        ),
        # Bottom player (Position 0 - East) - larger display
        rx.box(
            rx.vstack(
                rx.box(
                    rx.text("Discards:", font_size="sm", font_weight="600", color="#718096", margin_bottom="8px"),
                    render_player_discards(player_discards[0], size="normal"),
                    margin_bottom="16px",
                ),
                render_hand(
                    player_hands[0],
                    0,
                    player_names[0],
                    is_current=current_player == 0,
                    is_interactive=True,
                    can_ron=can_ron[0],
                    can_pon=can_pon[0],
                    can_chi=can_chi[0],
                    can_kan=can_kan[0],
                    last_drawn_tile=player_last_drawn[0],
                    tile_size="normal",
                ),
                render_melds(player_melds[0]),
                spacing="3",
                align="center",
            ),
            position="absolute",
            bottom="0",
            left="50%",
            transform="translateX(-50%)",
            width="100%",
            max_width="900px",
        ),
        position="relative",
        min_height="800px",
        width="100%",
        padding="20px",
    )
