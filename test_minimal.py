"""Minimal test to verify Reflex works"""
import reflex as rx

class State(rx.State):
    count: int = 0
    
    def increment(self):
        self.count += 1

def index() -> rx.Component:
    return rx.container(
        rx.heading("Test Page", size="9"),
        rx.text(f"Count: {State.count}"),
        rx.button("Click me", on_click=State.increment),
    )

app = rx.App()
app.add_page(index)
