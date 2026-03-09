"""
Reflex configuration file.
"""

import reflex as rx


config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    # Disable sitemap plugin for now
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
