"""
UI components for rendering the game board and discard piles.
"""

import reflex as rx
from typing import List


def render_discard_pile(discards: List[str], player_name: str) -> rx.Component:
    """
    Render a player's discard pile (河).

    Args:
        discards: List of discarded tile strings
        player_name: Name/position of the player

    Returns:
        Reflex component for the discard pile
    """
    return rx.box(
        rx.text(f"{player_name}'s discards:", font_weight="bold", margin_bottom="4px"),
        rx.cond(
            discards.length() > 0,
            rx.hstack(
                rx.foreach(
                    discards,
                    lambda tile: rx.box(
                        tile,
                        padding="4px 8px",
                        border="1px solid #cbd5e0",
                        border_radius="3px",
                        background="#edf2f7",
                        font_size="14px",
                        font_family="monospace",
                        margin="1px",
                    )
                ),
                spacing="1",
                wrap="wrap",
            ),
            rx.text("(none)", color="gray"),
        ),
        padding="12px",
        border_radius="6px",
        background="#f7fafc",
        margin="8px",
    )


def render_board(
    current_player: int,
    current_player_name: str,
    wall_remaining: int,
    turn_count: int,
    dora_indicators: List[str],
) -> rx.Component:
    """
    Render the game board with status information.

    Args:
        current_player: Index of current player
        current_player_name: Name of current player
        wall_remaining: Number of tiles left in wall
        turn_count: Current turn number
        dora_indicators: List of dora indicator tiles

    Returns:
        Reflex component for the board
    """
    return rx.box(
        rx.vstack(
            rx.heading("Game Board", size="6", color="#2d3748"),
            rx.divider(),
            rx.hstack(
                rx.box(
                    rx.text("Current Player", font_size="sm", color="gray"),
                    rx.text(current_player_name, font_size="2xl", font_weight="bold"),
                    rx.text("Position " + current_player.to_string(), font_size="xs", color="gray"),
                    padding="12px",
                    border="1px solid #e2e8f0",
                    border_radius="8px",
                ),
                rx.box(
                    rx.text("Turn", font_size="sm", color="gray"),
                    rx.text(turn_count, font_size="2xl", font_weight="bold"),
                    padding="12px",
                    border="1px solid #e2e8f0",
                    border_radius="8px",
                ),
                rx.box(
                    rx.text("Wall Remaining", font_size="sm", color="gray"),
                    rx.text(wall_remaining, font_size="2xl", font_weight="bold"),
                    rx.text(wall_remaining.to_string() + " tiles left", font_size="xs", color="gray"),
                    padding="12px",
                    border="1px solid #e2e8f0",
                    border_radius="8px",
                ),
                spacing="4",
            ),
            rx.divider(),
            rx.hstack(
                rx.text("Dora Indicators:", font_weight="bold"),
                rx.foreach(
                    dora_indicators,
                    lambda tile: rx.badge(tile, color_scheme="red", font_size="16px")
                ),
                spacing="2",
            ),
            spacing="4",
        ),
        padding="20px",
        border_radius="12px",
        background="white",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
        margin="16px",
    )


def render_game_controls() -> rx.Component:
    """
    Render game control buttons.

    Returns:
        Reflex component for game controls
    """
    from ..state import MahjongState

    return rx.vstack(
        rx.hstack(
            rx.button(
                "New Game",
                on_click=MahjongState.start_new_game,
                color_scheme="blue",
                size="3",
            ),
            rx.button(
                "Check Tenpai",
                on_click=MahjongState.check_current_tenpai,
                color_scheme="green",
                size="3",
            ),
            rx.button(
                "Declare Riichi",
                on_click=MahjongState.declare_riichi,
                color_scheme="orange",
                size="3",
            ),
            rx.button(
                "Export Log",
                on_click=MahjongState.export_log,
                color_scheme="purple",
                size="3",
            ),
            spacing="4",
        ),
        # Ron/Tsumo action buttons
        rx.cond(
            MahjongState.can_tsumo,
            rx.hstack(
                rx.button(
                    "🎉 TSUMO! (Self-Draw Win)",
                    on_click=MahjongState.declare_tsumo,
                    color_scheme="red",
                    size="4",
                    variant="solid",
                ),
                spacing="4",
            ),
            rx.box(),
        ),
        spacing="4",
        padding="16px",
        width="100%",
    )


def render_info_panel(info_message: str, waiting_tiles: List[str]) -> rx.Component:
    """
    Render information panel showing messages and waiting tiles.

    Args:
        info_message: Message to display
        waiting_tiles: Tiles the current player is waiting for

    Returns:
        Reflex component for info panel
    """
    return rx.box(
        rx.vstack(
            rx.cond(
                info_message.length() > 0,
                rx.callout(
                    info_message,
                    icon="info",
                    color_scheme="blue",
                ),
                rx.box(),
            ),
            rx.cond(
                waiting_tiles.length() > 0,
                rx.box(
                    rx.text("Waiting for:", font_weight="bold", margin_bottom="4px"),
                    rx.hstack(
                        rx.foreach(
                            waiting_tiles,
                            lambda tile: rx.badge(tile, color_scheme="green", font_size="16px")
                        ),
                        spacing="2",
                    ),
                    padding="12px",
                    border_radius="8px",
                    background="#f0fff4",
                    border="2px solid #48bb78",
                ),
                rx.box(),
            ),
            spacing="4",
        ),
        padding="16px",
        margin="8px",
    )
