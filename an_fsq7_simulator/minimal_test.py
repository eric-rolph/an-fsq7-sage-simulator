"""Minimal test to isolate the React error"""

import reflex as rx

class SimpleState(rx.State):
    message: str = "Hello from SAGE Simulator!"
    counter: int = 0
    
    def increment(self):
        self.counter += 1

def simple_page():
    return rx.container(
        rx.vstack(
            rx.heading("SAGE Simulator - Minimal Test", size="9", color="#00ff00"),
            rx.text(SimpleState.message, color="#88ff88"),
            rx.text(f"Counter: {SimpleState.counter}", color="#ffff00"),
            rx.button("Increment", on_click=SimpleState.increment),
            spacing="4",
            padding="2rem"
        ),
        background="#000000",
        min_height="100vh"
    )

app = rx.App()
app.add_page(simple_page, route="/test")
