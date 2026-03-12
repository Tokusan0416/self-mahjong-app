"""
Main Reflex application for Mahjong self-play simulator.
"""

import reflex as rx
from .state import MahjongState
from .components.hand import render_hand, render_melds
from .components.board import (
    render_board,
    render_discard_pile,
    render_game_controls,
    render_info_panel,
)
from .components.exhaustive_draw_display import render_exhaustive_draw_overlay
from .components.game_end_screen import render_game_end_screen
from .components.mahjong_table import render_mahjong_table


def index() -> rx.Component:
    """Main page component."""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading(
                "🀄 Mahjong Self-Play Simulator",
                size="9",
                margin_bottom="8px",
                text_align="center",
            ),
            rx.text(
                "Practice Mahjong by playing all 4 positions yourself",
                color="gray",
                text_align="center",
                margin_bottom="16px",
            ),
            rx.divider(),
            # Game controls
            render_game_controls(),
            rx.divider(),
            # Info panel
            render_info_panel(
                MahjongState.info_message,
                MahjongState.waiting_tiles,
            ),
            # Game board
            render_board(
                MahjongState.current_player,
                MahjongState.current_player_name,
                MahjongState.wall_remaining,
                MahjongState.turn_count,
                MahjongState.dora_indicators,
                MahjongState.round_name,
                MahjongState.game_type_label,
            ),
            rx.divider(),
            # Pass on calls button (shown when any call is available)
            rx.cond(
                MahjongState.can_ron[0] | MahjongState.can_ron[1] | MahjongState.can_ron[2] | MahjongState.can_ron[3] |
                MahjongState.can_pon[0] | MahjongState.can_pon[1] | MahjongState.can_pon[2] | MahjongState.can_pon[3] |
                MahjongState.can_chi[0] | MahjongState.can_chi[1] | MahjongState.can_chi[2] | MahjongState.can_chi[3] |
                MahjongState.can_kan[0] | MahjongState.can_kan[1] | MahjongState.can_kan[2] | MahjongState.can_kan[3],
                rx.center(
                    rx.button(
                        "Pass on All Calls (Continue Game)",
                        on_click=MahjongState.pass_on_ron,
                        color_scheme="gray",
                        size="3",
                        variant="outline",
                    ),
                    padding="8px",
                ),
                rx.box(),
            ),
            # Mahjong table with cross-pattern layout
            render_mahjong_table(
                # Player data
                player_hands=MahjongState.player_hands,
                player_names=MahjongState.player_names,
                player_discards=MahjongState.player_discards,
                player_melds=MahjongState.player_melds,
                player_last_drawn=MahjongState.player_last_drawn,
                current_player=MahjongState.current_player,
                # Call availability
                can_ron=MahjongState.can_ron,
                can_pon=MahjongState.can_pon,
                can_chi=MahjongState.can_chi,
                can_kan=MahjongState.can_kan,
            ),
            rx.divider(),
            # Footer
            rx.center(
                rx.text(
                    "Built with Reflex • For game analysis and ML training data",
                    color="gray",
                    font_size="sm",
                ),
                padding="16px",
            ),
            spacing="4",
            width="100%",
        ),
        # Exhaustive draw overlay (shown when is_exhaustive_draw is true)
        rx.cond(
            MahjongState.is_exhaustive_draw,
            render_exhaustive_draw_overlay(
                MahjongState.tenpai_players,
                MahjongState.player_names,
                MahjongState.player_scores,
                MahjongState.continue_after_exhaustive_draw,
            ),
            rx.box(),
        ),
        # Game end screen (shown when game is over)
        rx.cond(
            MahjongState.is_game_over,
            render_game_end_screen(
                MahjongState.player_names,
                MahjongState.player_scores,
                MahjongState.player_rankings,
                MahjongState.game_type_label,
                MahjongState.start_new_game_hanchan,
                MahjongState.start_new_game_tonpuu,
            ),
            rx.box(),
        ),
        max_width="1400px",
        padding="20px",
    )


# Create the app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
    )
)

# Add the index page
app.add_page(index, route="/", title="Mahjong Self-Play Simulator")
