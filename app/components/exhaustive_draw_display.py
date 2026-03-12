"""
Exhaustive draw (流局) display component.
"""

import reflex as rx
from typing import List, Callable


def render_exhaustive_draw_overlay(
    tenpai_players: List[int],
    player_names: List[str],
    player_scores: List[int],
    on_continue: Callable = None,
) -> rx.Component:
    """
    Render overlay showing tenpai/noten status after exhaustive draw.

    Args:
        tenpai_players: List of player indices who are in tenpai
        player_names: Names of all players
        player_scores: Current scores of all players

    Returns:
        Reflex component for exhaustive draw overlay
    """
    # Use .length() for Reflex Vars instead of len()
    num_tenpai = tenpai_players.length()

    # Create player status items
    player_status_items = []
    for i in range(4):
        # Use .contains() for membership test on Reflex Vars
        is_tenpai = tenpai_players.contains(i)

        player_status_items.append(
            rx.hstack(
                rx.cond(
                    is_tenpai,
                    rx.text(
                        "✓",
                        font_size="xl",
                        font_weight="bold",
                        color="#38a169",
                        width="30px",
                    ),
                    rx.text(
                        "✗",
                        font_size="xl",
                        font_weight="bold",
                        color="#e53e3e",
                        width="30px",
                    ),
                ),
                rx.text(
                    player_names[i],
                    font_weight="bold",
                    width="80px",
                ),
                rx.cond(
                    is_tenpai,
                    rx.text(
                        "テンパイ (Tenpai)",
                        color="#38a169",
                        font_weight="600",
                        width="150px",
                    ),
                    rx.text(
                        "ノーテン (Noten)",
                        color="#e53e3e",
                        font_weight="600",
                        width="150px",
                    ),
                ),
                rx.text(
                    f"{player_scores[i]:,}点",
                    font_size="sm",
                    color="#718096",
                ),
                spacing="3",
                align="center",
            )
        )

    return rx.box(
        # Semi-transparent backdrop
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            background_color="rgba(0, 0, 0, 0.6)",
            z_index="1000",
        ),
        # Modal content
        rx.box(
            rx.vstack(
                # Title
                rx.heading(
                    "流局 (Exhaustive Draw)",
                    size="7",
                    color="#2c5282",
                    margin_bottom="1em",
                ),
                # Tenpai count
                rx.text(
                    f"Tenpai: {num_tenpai} players, Noten: {4 - num_tenpai} players",
                    font_size="lg",
                    color="#4a5568",
                    margin_bottom="1em",
                ),
                # Payment info (show if 0 < tenpai < 4)
                rx.cond(
                    (num_tenpai > 0) & (num_tenpai < 4),
                    rx.text(
                        "Noten payment: 3000 points distributed from noten to tenpai players",
                        font_size="md",
                        color="#d69e2e",
                        font_weight="600",
                        margin_bottom="1.5em",
                    ),
                    rx.box(),
                ),
                # Player status
                rx.vstack(
                    *player_status_items,
                    spacing="3",
                    width="100%",
                    margin_bottom="2em",
                ),
                # Continue button
                rx.button(
                    "次の局へ (Continue to Next Round)",
                    on_click=on_continue,
                    size="3",
                    color_scheme="blue",
                    width="100%",
                ),
                spacing="4",
                align="center",
            ),
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            background_color="white",
            padding="2em",
            border_radius="12px",
            box_shadow="0 10px 40px rgba(0, 0, 0, 0.3)",
            z_index="1001",
            max_width="600px",
            width="90%",
        ),
    )
