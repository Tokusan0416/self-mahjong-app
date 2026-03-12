"""
Mahjong table layout component - cross pattern with center discard area.
"""

import reflex as rx
from typing import List


def render_center_discard_area(
    player_discards: List[List[str]],
    player_names: List[str],
) -> rx.Component:
    """
    Render center discard area showing all players' discards.

    Args:
        player_discards: List of discard piles for each player
        player_names: Names of all players

    Returns:
        Reflex component for center discard area
    """
    return rx.box(
        rx.vstack(
            rx.text(
                "捨て牌エリア (Discard Area)",
                font_size="sm",
                font_weight="bold",
                color="#718096",
                margin_bottom="8px",
            ),
            # Grid showing all 4 players' discards
            rx.grid(
                # Top player (Position 2)
                _render_discard_section(player_discards[2], player_names[2], "top"),
                # Left player (Position 3)
                _render_discard_section(player_discards[3], player_names[3], "left"),
                # Right player (Position 1)
                _render_discard_section(player_discards[1], player_names[1], "right"),
                # Bottom player (Position 0)
                _render_discard_section(player_discards[0], player_names[0], "bottom"),
                columns="2",
                spacing="2",
                width="100%",
            ),
            align="center",
            padding="16px",
            border="2px solid #e2e8f0",
            border_radius="8px",
            background_color="#f7fafc",
            width="100%",
            max_width="600px",
        ),
    )


def _render_discard_section(
    discards: List[str],
    player_name: str,
    position: str,
) -> rx.Component:
    """
    Render a single player's discard section in the center area.

    Args:
        discards: List of discarded tiles
        player_name: Player name
        position: Position label (top/bottom/left/right)

    Returns:
        Reflex component for discard section
    """
    return rx.box(
        rx.vstack(
            rx.text(
                player_name,
                font_size="xs",
                font_weight="600",
                color="#4a5568",
            ),
            rx.box(
                rx.hstack(
                    rx.foreach(
                        discards,
                        lambda tile: rx.text(
                            tile,
                            font_size="xs",
                            padding="2px 4px",
                            background_color="#ffffff",
                            border="1px solid #cbd5e0",
                            border_radius="2px",
                        ),
                    ),
                    spacing="1",
                    wrap="wrap",
                ),
                min_height="30px",
                max_width="150px",
                overflow="hidden",
            ),
            spacing="1",
            align="center",
        ),
        padding="8px",
        background_color="#ffffff",
        border_radius="4px",
        border="1px solid #e2e8f0",
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
        Top: Player 2 (West)
        Right: Player 1 (South)
        Bottom: Player 0 (East) - larger display
        Left: Player 3 (North)
        Center: Discard area

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
                spacing="2",
                align="center",
            ),
            position="absolute",
            top="0",
            left="50%",
            transform="translateX(-50%)",
            width="100%",
            max_width="600px",
        ),
        # Middle row: Left, Center, Right
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
                    spacing="2",
                    align="center",
                ),
                width="200px",
            ),
            # Center discard area
            rx.box(
                render_center_discard_area(player_discards, player_names),
                flex="1",
                display="flex",
                justify_content="center",
                align_items="center",
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
                    spacing="2",
                    align="center",
                ),
                width="200px",
            ),
            spacing="4",
            align="center",
            justify="between",
            width="100%",
            margin_top="120px",
            margin_bottom="20px",
        ),
        # Bottom player (Position 0 - East) - larger display
        rx.box(
            rx.vstack(
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
            max_width="800px",
        ),
        position="relative",
        min_height="700px",
        width="100%",
        padding="20px",
    )
