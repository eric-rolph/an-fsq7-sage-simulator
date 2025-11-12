import reflex as rx
import os

# Disable hot reload on Windows to prevent premature shutdown
os.environ["REFLEX_DISABLE_HOT_RELOAD"] = "1"

config = rx.Config(
    app_name="an_fsq7_simulator",
    app_module_import="an_fsq7_simulator.interactive_sage",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
)
