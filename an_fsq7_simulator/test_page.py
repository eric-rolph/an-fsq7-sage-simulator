"""
Minimal test page to verify server stability
"""

import reflex as rx


class TestState(rx.State):
    """Minimal test state"""
    counter: int = 0
    
    def increment(self):
        self.counter += 1


def test_page() -> rx.Component:
    """Simple test page"""
    return rx.container(
        rx.vstack(
            rx.heading("SAGE Simulator - Test Page", size="9", color="#00ff00"),
            rx.text("If you can see this, the server is working!"),
            rx.text(f"Counter: {TestState.counter}"),
            rx.button("Increment", on_click=TestState.increment),
            spacing="4",
            padding="20px"
        ),
        background="#000000"
    )


# Create app
app = rx.App()
app.add_page(test_page, route="/test")
