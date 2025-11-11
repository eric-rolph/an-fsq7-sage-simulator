import reflex as rx

config = rx.Config(
    app_name="an_fsq7_simulator",
    app_module_import="an_fsq7_simulator.test_page",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
