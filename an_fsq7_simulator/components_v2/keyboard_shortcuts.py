"""
Keyboard Shortcuts & Accessibility System

Provides global keyboard navigation and shortcuts for the SAGE simulator.
Implements WCAG 2.1 Level AA accessibility requirements.

Keyboard Shortcuts:
- D: Toggle light gun arm/disarm
- SPACE: Context-sensitive quick action (launch, classify, etc.)
- TAB: Navigate through interactive elements
- ESC: Dismiss active panel/modal
- ?: Show keyboard shortcuts help
- Shift+I: Toggle system inspector overlay
- Shift+P: Toggle performance overlay
- Shift+N: Toggle network/stations view
- 1-7: Quick select scenario (when in scenario selector)
- Enter: Confirm action / Start scenario
- Arrow Keys: Navigate lists/options

Focus Management:
- Visible focus indicators on all interactive elements
- Focus trap for modal dialogs
- Skip to main content link
- Logical tab order

Screen Reader Support:
- ARIA labels for all controls
- ARIA live regions for dynamic content
- ARIA pressed/expanded states
- Semantic HTML structure
"""

import reflex as rx
from typing import Optional


# Keyboard shortcut definitions
KEYBOARD_SHORTCUTS = {
    "Navigation": [
        ("Tab", "Navigate to next interactive element"),
        ("Shift+Tab", "Navigate to previous element"),
        ("Esc", "Dismiss active panel or modal"),
        ("?", "Show this keyboard shortcuts help"),
    ],
    "Light Gun & Selection": [
        ("D", "Toggle light gun arm/disarm"),
        ("Click (with light gun armed)", "Select track on radar"),
        ("C", "Clear track selection"),
    ],
    "Track Operations": [
        ("H", "Classify selected track as Hostile"),
        ("F", "Classify selected track as Friendly"),
        ("U", "Mark selected track as Unknown"),
        ("Space", "Quick action (context-sensitive)"),
    ],
    "Interceptor Control": [
        ("A", "Assign interceptor to selected hostile track"),
        ("L", "Launch assigned interceptor"),
        ("Enter", "Confirm interceptor assignment"),
    ],
    "Scenario Management": [
        ("1-7", "Quick select scenario (in scenario selector)"),
        ("S", "Start selected scenario"),
        ("P", "Pause/Resume scenario"),
        ("R", "Reset scenario"),
    ],
    "System Views": [
        ("Shift+I", "Toggle System Inspector overlay"),
        ("Shift+P", "Toggle Performance overlay"),
        ("Shift+N", "Toggle Network/Stations view"),
        ("Shift+M", "Toggle System Messages panel"),
    ],
}


def keyboard_help_panel(on_close=None) -> rx.Component:
    """
    Keyboard shortcuts help overlay.
    
    Shows when user presses '?' key. Displays all available keyboard shortcuts
    organized by category with descriptions.
    
    Args:
        on_close: Event handler for closing the panel (optional)
    """
    
    def shortcut_row(key: str, description: str) -> rx.Component:
        return rx.hstack(
            rx.box(
                rx.text(
                    key,
                    font_family="monospace",
                    font_weight="bold",
                    color="var(--accent-9)",
                ),
                bg="var(--gray-3)",
                px="8px",
                py="4px",
                border_radius="4px",
                border="1px solid var(--gray-6)",
                min_width="120px",
            ),
            rx.text(
                description,
                color="var(--gray-11)",
                flex="1",
            ),
            spacing="3",
            width="100%",
            align="center",
        )
    
    def category_section(category: str, shortcuts: list) -> rx.Component:
        return rx.vstack(
            rx.heading(
                category,
                size="3",
                color="var(--accent-11)",
                margin_bottom="8px",
            ),
            *[shortcut_row(key, desc) for key, desc in shortcuts],
            spacing="2",
            width="100%",
            align="start",
        )
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "⌨️ Keyboard Shortcuts",
                    size="5",
                    color="var(--gray-12)",
                ),
                rx.icon_button(
                    rx.icon("x"),
                    on_click=on_close if on_close else lambda: None,
                    size="2",
                    variant="ghost",
                    aria_label="Close keyboard shortcuts help",
                    id="keyboard-help-close-button",
                ),
                justify="between",
                width="100%",
                margin_bottom="16px",
            ),
            
            # Shortcuts by category
            rx.scroll_area(
                rx.vstack(
                    *[
                        category_section(category, shortcuts)
                        for category, shortcuts in KEYBOARD_SHORTCUTS.items()
                    ],
                    spacing="5",
                    width="100%",
                ),
                height="500px",
                type="always",
            ),
            
            # Footer
            rx.hstack(
                rx.text(
                    "Press Esc or ? to close this help panel",
                    color="var(--gray-10)",
                    size="2",
                    font_style="italic",
                ),
                justify="center",
                width="100%",
                margin_top="16px",
            ),
            
            spacing="0",
            width="100%",
        ),
        position="fixed",
        top="50%",
        left="50%",
        transform="translate(-50%, -50%)",
        bg="var(--color-panel)",
        border="2px solid var(--accent-9)",
        border_radius="12px",
        box_shadow="0 8px 32px rgba(0, 0, 0, 0.4)",
        padding="24px",
        width="700px",
        max_width="90vw",
        max_height="90vh",
        z_index="9999",
        role="dialog",
        aria_label="Keyboard shortcuts help",
        aria_modal="true",
    )


def keyboard_shortcuts_script() -> str:
    """
    JavaScript for global keyboard event handling.
    
    Returns:
        JavaScript code as string to be injected via rx.html()
    """
    return """
<script>
(function() {
    'use strict';
    
    console.log('[Keyboard] Initializing keyboard shortcuts system');
    
    // Prevent multiple initializations
    if (window.__SAGE_KEYBOARD_INITIALIZED__) {
        console.log('[Keyboard] Already initialized, skipping');
        return;
    }
    window.__SAGE_KEYBOARD_INITIALIZED__ = true;
    
    // Track current focus for accessibility
    let currentFocusIndex = -1;
    let focusableElements = [];
    
    /**
     * Get all focusable elements in the document
     */
    function updateFocusableElements() {
        focusableElements = Array.from(document.querySelectorAll(
            'button:not([disabled]), ' +
            'a[href], ' +
            'input:not([disabled]), ' +
            'select:not([disabled]), ' +
            'textarea:not([disabled]), ' +
            '[tabindex]:not([tabindex="-1"])'
        ));
        console.log(`[Keyboard] Found ${focusableElements.length} focusable elements`);
    }
    
    /**
     * Focus next/previous element
     */
    function moveFocus(direction) {
        if (focusableElements.length === 0) {
            updateFocusableElements();
        }
        
        currentFocusIndex += direction;
        
        if (currentFocusIndex < 0) {
            currentFocusIndex = focusableElements.length - 1;
        } else if (currentFocusIndex >= focusableElements.length) {
            currentFocusIndex = 0;
        }
        
        if (focusableElements[currentFocusIndex]) {
            focusableElements[currentFocusIndex].focus();
            console.log('[Keyboard] Focused element:', focusableElements[currentFocusIndex].getAttribute('aria-label') || focusableElements[currentFocusIndex].tagName);
        }
    }
    
    /**
     * Find and click button by text content or aria-label
     */
    function clickButtonByText(text) {
        const buttons = Array.from(document.querySelectorAll('button'));
        const button = buttons.find(btn => 
            btn.textContent.includes(text) || 
            (btn.getAttribute('aria-label') || '').includes(text)
        );
        
        if (button && !button.disabled) {
            console.log('[Keyboard] Clicking button:', text);
            button.click();
            return true;
        }
        return false;
    }
    
    /**
     * Global keyboard event handler
     */
    function handleKeyDown(event) {
        const key = event.key;
        const ctrl = event.ctrlKey;
        const shift = event.shiftKey;
        const alt = event.altKey;
        
        // Get active element to check context
        const activeElement = document.activeElement;
        const isInputField = activeElement && (
            activeElement.tagName === 'INPUT' ||
            activeElement.tagName === 'TEXTAREA' ||
            activeElement.isContentEditable
        );
        
        // Don't intercept keys in input fields (except Escape)
        if (isInputField && key !== 'Escape') {
            return;
        }
        
        // Handle keyboard shortcuts
        let handled = false;
        
        // Help overlay (?) - Toggle by clicking hidden button
        if (key === '?' && !ctrl && !alt) {
            console.log('[Keyboard] Toggle help overlay');
            const toggleButton = document.getElementById('keyboard-help-toggle-button');
            if (toggleButton) {
                toggleButton.click();
                handled = true;
            } else {
                console.warn('[Keyboard] Help toggle button not found');
            }
        }
        
        // Escape - dismiss panels
        else if (key === 'Escape' && !ctrl && !alt) {
            console.log('[Keyboard] Dismiss active panels');
            // Close keyboard help if open by clicking the visible close button
            const closeButton = document.getElementById('keyboard-help-close-button');
            if (closeButton) {
                closeButton.click();
                handled = true;
            }
            // Trigger dismiss event via hidden button
            const dismissButton = document.getElementById('keyboard-dismiss-button');
            if (dismissButton) {
                dismissButton.click();
                handled = true;
            }
            // Also dispatch event for client-side listeners
            window.dispatchEvent(new CustomEvent('sage:dismiss-panels'));
        }
        
        // D - Toggle light gun
        else if (key === 'd' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Toggle light gun');
            handled = clickButtonByText('ARM LIGHT GUN') || clickButtonByText('DISARM');
        }
        
        // Shift+I - System Inspector
        else if (key === 'I' && shift && !ctrl && !alt) {
            console.log('[Keyboard] Toggle system inspector');
            const inspectorButton = document.getElementById('keyboard-inspector-toggle-button');
            if (inspectorButton) {
                inspectorButton.click();
                handled = true;
            }
            window.dispatchEvent(new CustomEvent('sage:toggle-inspector'));
        }
        
        // Shift+P - Performance overlay
        else if (key === 'P' && shift && !ctrl && !alt) {
            console.log('[Keyboard] Toggle performance overlay');
            const perfButton = document.getElementById('keyboard-performance-toggle-button');
            if (perfButton) {
                perfButton.click();
                handled = true;
            }
            window.dispatchEvent(new CustomEvent('sage:toggle-performance'));
        }
        
        // Shift+N - Network view
        else if (key === 'N' && shift && !ctrl && !alt) {
            console.log('[Keyboard] Toggle network view');
            handled = clickButtonByText('NETWORK') || clickButtonByText('RADAR');
        }
        
        // Space - Context-sensitive action
        else if (key === ' ' && !ctrl && !alt && !shift && !isInputField) {
            console.log('[Keyboard] Context-sensitive action (Space)');
            // Try to click the most relevant button based on context
            handled = clickButtonByText('LAUNCH') || 
                      clickButtonByText('ASSIGN') ||
                      clickButtonByText('HOSTILE') ||
                      clickButtonByText('VIEW DETAILS') ||
                      clickButtonByText('START');
        }
        
        // H - Classify as Hostile
        else if (key === 'h' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Classify as hostile');
            handled = clickButtonByText('HOSTILE');
        }
        
        // F - Classify as Friendly
        else if (key === 'f' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Classify as friendly');
            handled = clickButtonByText('FRIENDLY');
        }
        
        // U - Mark as Unknown
        else if (key === 'u' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Mark as unknown');
            handled = clickButtonByText('UNKNOWN');
        }
        
        // C - Clear selection
        else if (key === 'c' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Clear selection');
            handled = clickButtonByText('CLEAR') || clickButtonByText('CANCEL');
        }
        
        // A - Assign interceptor
        else if (key === 'a' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Assign interceptor');
            handled = clickButtonByText('ASSIGN');
        }
        
        // L - Launch interceptor
        else if (key === 'l' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Launch interceptor');
            handled = clickButtonByText('LAUNCH');
        }
        
        // P - Pause/Resume (without shift)
        else if (key === 'p' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Toggle pause');
            handled = clickButtonByText('PAUSE') || clickButtonByText('RESUME');
        }
        
        // S - Start scenario
        else if (key === 's' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Start scenario');
            handled = clickButtonByText('START');
        }
        
        // R - Reset scenario
        else if (key === 'r' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Reset scenario');
            handled = clickButtonByText('RESET');
        }
        
        // 1-7 - Quick select scenario
        else if (/^[1-7]$/.test(key) && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Quick select scenario:', key);
            // Find scenario button by index
            const scenarioButtons = Array.from(document.querySelectorAll('button')).filter(btn =>
                btn.textContent.includes('Demo') || btn.textContent.includes('Scenario')
            );
            const index = parseInt(key) - 1;
            if (scenarioButtons[index]) {
                scenarioButtons[index].click();
                handled = true;
            }
        }
        
        // Enter - Confirm/Launch/Start
        else if (key === 'Enter' && !ctrl && !alt && !shift) {
            console.log('[Keyboard] Enter key pressed');
            handled = clickButtonByText('CONFIRM') || 
                      clickButtonByText('LAUNCH') || 
                      clickButtonByText('START') ||
                      clickButtonByText('NEW CONTACT');
        }
        
        // Tab navigation (update focusable elements list)
        if (key === 'Tab') {
            updateFocusableElements();
        }
        
        // Prevent default if we handled the key
        if (handled) {
            event.preventDefault();
            event.stopPropagation();
        }
    }
    
    // Attach global keyboard listener
    document.addEventListener('keydown', handleKeyDown, true);
    
    // Update focusable elements on page changes
    const observer = new MutationObserver(() => {
        updateFocusableElements();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });
    
    // Initial update
    updateFocusableElements();
    
    console.log('[Keyboard] ✓ Keyboard shortcuts system initialized');
})();
</script>
    """.strip()


def focus_styles_css() -> str:
    """
    CSS for visible focus indicators.
    
    Returns:
        CSS code as string to be injected via rx.html()
    """
    return """
<style>
/* Visible focus indicators for accessibility */
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
[tabindex]:focus-visible {
    outline: 3px solid var(--accent-9) !important;
    outline-offset: 2px !important;
    box-shadow: 0 0 0 4px var(--accent-a3) !important;
}

/* Focus within containers */
*:focus-within {
    /* Container has focused child */
}

/* Skip to main content link */
.skip-to-main {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--accent-9);
    color: white;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 0 0 4px 0;
    z-index: 10000;
    font-weight: bold;
}

.skip-to-main:focus {
    top: 0;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    button:focus-visible,
    a:focus-visible,
    input:focus-visible {
        outline-width: 4px !important;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
    """.strip()


def keyboard_shortcuts_component(
    keyboard_help_visible_var, 
    on_close_help=None,
    on_toggle_inspector=None,
    on_toggle_performance=None,
    on_dismiss_panels=None
) -> rx.Component:
    """
    Main keyboard shortcuts component.
    
    Injects JavaScript and CSS for keyboard handling and focus management.
    Includes conditional keyboard help panel.
    
    Args:
        keyboard_help_visible_var: Reflex Var for keyboard_help_visible state
        on_close_help: Event handler for closing the help panel (optional)
        on_toggle_inspector: Event handler for toggling system inspector
        on_toggle_performance: Event handler for toggling performance overlay
        on_dismiss_panels: Event handler for dismissing panels (Esc)
    
    Returns:
        Reflex component with keyboard functionality
    """
    return rx.fragment(
        # Inject keyboard handling JavaScript
        rx.html(keyboard_shortcuts_script()),
        
        # Inject focus styles CSS
        rx.html(focus_styles_css()),
        
        # Skip to main content link (accessibility)
        rx.html(
            '<a href="#main-content" class="skip-to-main">Skip to main content</a>'
        ),
        
        # Hidden button for toggling help via JavaScript (? key)
        # This button is always present but invisible, allowing JavaScript to trigger the state change
        rx.button(
            id="keyboard-help-toggle-button",
            on_click=on_close_help,
            style={"display": "none"},  # Completely hidden from UI
            aria_hidden="true",
        ),
        
        # Hidden buttons for other global shortcuts
        rx.button(
            id="keyboard-inspector-toggle-button",
            on_click=on_toggle_inspector,
            style={"display": "none"},
            aria_hidden="true",
        ),
        rx.button(
            id="keyboard-performance-toggle-button",
            on_click=on_toggle_performance,
            style={"display": "none"},
            aria_hidden="true",
        ),
        rx.button(
            id="keyboard-dismiss-button",
            on_click=on_dismiss_panels,
            style={"display": "none"},
            aria_hidden="true",
        ),
        
        # Keyboard help panel (shown conditionally)
        rx.cond(
            keyboard_help_visible_var,
            keyboard_help_panel(on_close=on_close_help),
        ),
    )
