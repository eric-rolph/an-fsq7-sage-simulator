import reflex as rx

config = rx.Config(
    app_name="an_fsq7_simulator",
    app_module_import="an_fsq7_simulator.interactive_sage",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
