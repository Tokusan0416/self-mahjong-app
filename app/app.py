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
            # All 4 players' hands in a grid
            rx.grid(
                # East (Position 0) - Bottom
                rx.box(
                    render_hand(
                        MahjongState.player_hands[0],
                        0,
                        MahjongState.player_names[0],
                        is_current=MahjongState.current_player == 0,
                        is_interactive=True,
                        can_ron=MahjongState.can_ron[0],
                        can_pon=MahjongState.can_pon[0],
                        can_chi=MahjongState.can_chi[0],
                        can_kan=MahjongState.can_kan[0],
                    ),
                    render_melds(MahjongState.player_melds[0]),
                    render_discard_pile(MahjongState.player_discards[0], "East"),
                ),
                # South (Position 1) - Right
                rx.box(
                    render_hand(
                        MahjongState.player_hands[1],
                        1,
                        MahjongState.player_names[1],
                        is_current=MahjongState.current_player == 1,
                        is_interactive=True,
                        can_ron=MahjongState.can_ron[1],
                        can_pon=MahjongState.can_pon[1],
                        can_chi=MahjongState.can_chi[1],
                        can_kan=MahjongState.can_kan[1],
                    ),
                    render_melds(MahjongState.player_melds[1]),
                    render_discard_pile(MahjongState.player_discards[1], "South"),
                ),
                # West (Position 2) - Top
                rx.box(
                    render_hand(
                        MahjongState.player_hands[2],
                        2,
                        MahjongState.player_names[2],
                        is_current=MahjongState.current_player == 2,
                        is_interactive=True,
                        can_ron=MahjongState.can_ron[2],
                        can_pon=MahjongState.can_pon[2],
                        can_chi=MahjongState.can_chi[2],
                        can_kan=MahjongState.can_kan[2],
                    ),
                    render_melds(MahjongState.player_melds[2]),
                    render_discard_pile(MahjongState.player_discards[2], "West"),
                ),
                # North (Position 3) - Left
                rx.box(
                    render_hand(
                        MahjongState.player_hands[3],
                        3,
                        MahjongState.player_names[3],
                        is_current=MahjongState.current_player == 3,
                        is_interactive=True,
                        can_ron=MahjongState.can_ron[3],
                        can_pon=MahjongState.can_pon[3],
                        can_chi=MahjongState.can_chi[3],
                        can_kan=MahjongState.can_kan[3],
                    ),
                    render_melds(MahjongState.player_melds[3]),
                    render_discard_pile(MahjongState.player_discards[3], "North"),
                ),
                columns="2",
                spacing="4",
                width="100%",
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
