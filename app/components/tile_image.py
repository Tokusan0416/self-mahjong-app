"""
Tile image component for rendering mahjong tiles as SVG images.
"""

import reflex as rx


# Tile code to SVG filename mapping
TILE_IMAGE_MAP = {
    # Manzu (萬子)
    "1m": "Man1.svg",
    "2m": "Man2.svg",
    "3m": "Man3.svg",
    "4m": "Man4.svg",
    "5m": "Man5.svg",
    "6m": "Man6.svg",
    "7m": "Man7.svg",
    "8m": "Man8.svg",
    "9m": "Man9.svg",
    # Pinzu (筒子)
    "1p": "Pin1.svg",
    "2p": "Pin2.svg",
    "3p": "Pin3.svg",
    "4p": "Pin4.svg",
    "5p": "Pin5.svg",
    "6p": "Pin6.svg",
    "7p": "Pin7.svg",
    "8p": "Pin8.svg",
    "9p": "Pin9.svg",
    # Souzu (索子)
    "1s": "Sou1.svg",
    "2s": "Sou2.svg",
    "3s": "Sou3.svg",
    "4s": "Sou4.svg",
    "5s": "Sou5.svg",
    "6s": "Sou6.svg",
    "7s": "Sou7.svg",
    "8s": "Sou8.svg",
    "9s": "Sou9.svg",
    # Jihai (字牌)
    "1z": "Ton.svg",    # 東 (East)
    "2z": "Nan.svg",    # 南 (South)
    "3z": "Shaa.svg",   # 西 (West)
    "4z": "Pei.svg",    # 北 (North)
    "5z": "Haku.svg",   # 白 (White dragon)
    "6z": "Hatsu.svg",  # 發 (Green dragon)
    "7z": "Chun.svg",   # 中 (Red dragon)
}


def get_tile_image_path(tile_str: str) -> str:
    """
    Get the image path for a tile code.

    Args:
        tile_str: Tile code (e.g., "1m", "5p", "1z")

    Returns:
        Path to the tile image
    """
    filename = TILE_IMAGE_MAP.get(tile_str, "Blank.svg")
    return f"/tiles/{filename}"


def render_tile_image(
    tile_str: str,
    size: str = "normal",
    is_clickable: bool = False,
    on_click=None,
) -> rx.Component:
    """
    Render a mahjong tile as an SVG image with text fallback.

    Args:
        tile_str: Tile code (e.g., "1m", "5p", "1z")
        size: Size variant ("normal" or "small")
        is_clickable: Whether the tile should have hover/click effects
        on_click: Click handler function

    Returns:
        Reflex component for the tile image
    """
    # Size configurations
    if size == "small":
        width = "32px"
        height = "42px"
        font_size = "10px"
        padding = "4px 6px"
    else:  # normal
        width = "40px"
        height = "56px"
        font_size = "14px"
        padding = "6px 8px"

    # Get image path
    image_path = get_tile_image_path(tile_str)

    # Hybrid display: image with text fallback
    tile_display = rx.box(
        # Try to show image first
        rx.image(
            src=image_path,
            alt=tile_str,
            width=width,
            height=height,
            object_fit="contain",
            display="block",
        ),
        # Text fallback (shown if image fails to load)
        rx.text(
            tile_str,
            position="absolute",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            font_size=font_size,
            font_weight="bold",
            color="#2d3748",
            font_family="monospace",
            text_align="center",
            z_index="1",
        ),
        position="relative",
        width=width,
        height=height,
        background="#ffffff",
        border="2px solid #333",
        border_radius="4px",
    )

    # Wrap in clickable box if needed
    if is_clickable and on_click:
        return rx.box(
            tile_display,
            on_click=on_click,
            cursor="pointer",
            border_radius="6px",
            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            _hover={
                "transform": "translateY(-4px) scale(1.05)",
                "box_shadow": "0 6px 12px rgba(44, 82, 130, 0.3)",
            },
            _active={
                "transform": "translateY(-2px) scale(1.02)",
                "box_shadow": "0 3px 6px rgba(44, 82, 130, 0.2)",
            },
        )
    else:
        return tile_display


def render_tile_static_image(
    tile_str: str,
    size: str = "normal",
) -> rx.Component:
    """
    Render a static (non-clickable) tile image.

    Args:
        tile_str: Tile code (e.g., "1m", "5p", "1z")
        size: Size variant ("normal" or "small")

    Returns:
        Reflex component for the static tile image
    """
    return render_tile_image(tile_str, size=size, is_clickable=False)


def render_tile_clickable_image(
    tile_str: str,
    player_idx: int,
    is_drawn_tile: bool = False,
    size: str = "normal",
) -> rx.Component:
    """
    Render a clickable tile image.

    Args:
        tile_str: Tile code (e.g., "1m", "5p", "1z")
        player_idx: Index of the player (0-3)
        is_drawn_tile: Whether this is the drawn tile
        size: Size variant ("normal" or "small")

    Returns:
        Reflex component for the clickable tile image
    """
    from ..state import MahjongState

    return render_tile_image(
        tile_str,
        size=size,
        is_clickable=True,
        on_click=lambda: MahjongState.discard_tile(player_idx, tile_str, is_drawn_tile),
    )
