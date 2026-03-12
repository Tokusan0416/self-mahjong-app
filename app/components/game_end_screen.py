"""
Game end screen component showing final scores and rankings.
"""

import reflex as rx
from typing import List, Callable


def render_game_end_screen(
    player_names: List[str],
    player_scores: List[int],
    player_rankings: List[int],
    game_type_label: str,
    on_new_game_hanchan: Callable = None,
    on_new_game_tonpuu: Callable = None,
) -> rx.Component:
    """
    Render game end screen with final scores and rankings.

    Args:
        player_names: Names of all players
        player_scores: Final scores of all players
        player_rankings: Rankings (1-4) for each player
        game_type_label: Game type label ("半荘" or "東風戦")
        on_new_game_hanchan: Handler for starting new hanchan game
        on_new_game_tonpuu: Handler for starting new tonpuu game

    Returns:
        Reflex component for game end screen
    """

    return rx.box(
        # Semi-transparent backdrop
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100%",
            background_color="rgba(0, 0, 0, 0.7)",
            z_index="1000",
        ),
        # Modal content
        rx.box(
            rx.vstack(
                # Title
                rx.heading(
                    "終局 (Game Over)",
                    size="8",
                    color="#2c5282",
                    margin_bottom="0.5em",
                ),
                rx.text(
                    f"Game Type: {game_type_label}",
                    font_size="lg",
                    color="#718096",
                    margin_bottom="1.5em",
                ),
                # Final Scores Header
                rx.heading(
                    "Final Scores & Rankings",
                    size="5",
                    color="#4a5568",
                    margin_bottom="1em",
                ),
                # Player rankings (sorted by score)
                rx.vstack(
                    # Player 0
                    _render_player_rank_row(player_names[0], player_scores[0], player_rankings[0]),
                    # Player 1
                    _render_player_rank_row(player_names[1], player_scores[1], player_rankings[1]),
                    # Player 2
                    _render_player_rank_row(player_names[2], player_scores[2], player_rankings[2]),
                    # Player 3
                    _render_player_rank_row(player_names[3], player_scores[3], player_rankings[3]),
                    spacing="3",
                    width="100%",
                    margin_bottom="2em",
                ),
                # Divider
                rx.divider(margin_y="1em"),
                # New game buttons
                rx.text(
                    "Start a New Game",
                    font_weight="bold",
                    color="#2d3748",
                    margin_bottom="0.5em",
                ),
                rx.hstack(
                    rx.button(
                        "New Game (半荘)",
                        on_click=on_new_game_hanchan,
                        size="3",
                        color_scheme="blue",
                        flex="1",
                    ),
                    rx.button(
                        "New Game (東風戦)",
                        on_click=on_new_game_tonpuu,
                        size="3",
                        color_scheme="cyan",
                        flex="1",
                    ),
                    spacing="3",
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
            padding="2.5em",
            border_radius="16px",
            box_shadow="0 20px 60px rgba(0, 0, 0, 0.4)",
            z_index="1001",
            max_width="700px",
            width="90%",
        ),
    )


def _render_player_rank_row(
    player_name: str,
    player_score: int,
    rank: int,
) -> rx.Component:
    """
    Render a single player's rank row.

    Args:
        player_name: Player name
        player_score: Player's final score
        rank: Player's rank (1-4)

    Returns:
        Reflex component for player rank row
    """
    # Rank colors and labels - use rx.match for conditional rendering
    rank_color = rx.match(
        rank,
        (1, "#d4af37"),  # Gold
        (2, "#c0c0c0"),  # Silver
        (3, "#cd7f32"),  # Bronze
        "#718096",  # Gray (default)
    )

    rank_label = rx.match(
        rank,
        (1, "🥇 1st"),
        (2, "🥈 2nd"),
        (3, "🥉 3rd"),
        "4th",  # default
    )

    # Score difference from 25000 (starting score)
    score_diff = player_score - 25000
    # Use rx.cond for conditional text and color
    diff_text = rx.cond(
        score_diff >= 0,
        f"+{score_diff}",
        f"{score_diff}",
    )
    diff_color = rx.cond(
        score_diff >= 0,
        "#38a169",
        "#e53e3e",
    )

    return rx.hstack(
        # Rank
        rx.box(
            rx.text(
                rank_label,
                font_size="xl",
                font_weight="bold",
                color=rank_color,
            ),
            width="100px",
        ),
        # Player name
        rx.text(
            player_name,
            font_weight="bold",
            font_size="lg",
            width="120px",
        ),
        # Score
        rx.text(
            f"{player_score:,}点",
            font_size="xl",
            font_weight="bold",
            color="#2d3748",
            flex="1",
        ),
        # Score difference
        rx.text(
            f"({diff_text})",
            font_size="md",
            color=diff_color,
            font_weight="600",
            width="100px",
            text_align="right",
        ),
        spacing="4",
        align="center",
        padding="12px",
        border_radius="8px",
        background_color=rx.cond(
            rank == 1,
            "rgba(212, 175, 55, 0.1)",
            rx.cond(
                rank == 2,
                "rgba(192, 192, 192, 0.1)",
                rx.cond(
                    rank == 3,
                    "rgba(205, 127, 50, 0.1)",
                    "rgba(113, 128, 150, 0.05)",
                )
            )
        ),
        width="100%",
    )
