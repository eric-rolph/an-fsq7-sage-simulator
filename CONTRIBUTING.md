# Contributing to AN/FSQ-7 SAGE Simulator

Thank you for your interest in contributing to this project! This guide will help you get started.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- UV package manager
- Git

### Setup
```powershell
# Clone the repository
git clone https://github.com/eric-rolph/an-fsq7-sage-simulator.git
cd an-fsq7-sage-simulator

# Run setup script (installs UV and dependencies)
.\setup.ps1  # Windows
# or
./setup.sh   # Linux/Mac

# Start development server
uv run reflex run
```

---

## 🧪 Testing Requirements

**CRITICAL:** All contributions must include tests and pass existing tests.

### Running Tests

```powershell
# Core unit tests (CPU, drum, light gun)
uv run pytest tests/unit

# Simulation tests (scenarios, physics)
uv run pytest tests/sim

# Design language / UI contract tests
uv run pytest tests/design_language

# Run all tests
uv run pytest
```

### Test Coverage Requirements
- **New Features:** Must have ≥80% test coverage
- **Bug Fixes:** Must include regression test
- **Refactoring:** All existing tests must pass

### Manual Testing Checklist
Before submitting a PR, verify:
- [ ] Server starts without errors: `uv run reflex run`
- [ ] Browser loads at http://localhost:3000
- [ ] No console errors in browser DevTools (F12)
- [ ] `window.__SAGE_*` globals populated
- [ ] Light gun selection works (press D, click target)
- [ ] Scenario debrief displays after mission
- [ ] No Python import errors: `uv run python -c "import an_fsq7_simulator.interactive_sage; print(\'OK\')"`

---

## 📐 Code Style Guidelines

### Python
- Follow PEP 8
- Use type hints for all function parameters and return values
- Document all classes and public methods with docstrings
- Use dataclasses for data structures

### JavaScript
- Use ES6+ syntax
- Add JSDoc comments for functions
- Use `const` by default, `let` only when needed
- Follow existing naming conventions (camelCase for variables, PascalCase for classes)

### Reflex-Specific Rules
**CRITICAL:** Review `agents.md` before coding - contains critical gotchas!

**Common Pitfalls:**
- **NEVER** use Python `and`/`or`/`not` on Reflex Var types → Use `|`, `&`, `~`
- **NEVER** use inline `if/else` on Reflex Vars → Use `rx.cond()`
- **ALWAYS** prefix commands with `uv run` (not `python` or `reflex` directly)
- **ALWAYS** use `@rx.var` for computed properties
- **ALWAYS** escape HTML in script tag injection: `html.escape(...)`

---

## 🎨 Design Language Invariants

**CRITICAL:** These rules MUST NOT be violated (see `agents.md` and `docs/UI_DESIGN_PATTERNS.md`):

### Mode-Free UI
- **NO hidden "modes"** - buttons should be disabled, not removed
- Track detail panel uses **ONE layout** for all track types
- Track type changes color/icon, NOT panel structure

### Layout Consistency
- Radar/scope is **central visual focus**
- Detail panel **always on right side** of main layout
- Global action controls in **consistent bottom/action region**
- **DO NOT** move detail panel based on state

### CRT Display (P14 Phosphor - HISTORICALLY ACCURATE)
- **Monochrome Display:** NO color coding - all symbology uses P14 orange phosphor
- **Track Symbols:** Differentiated by SHAPE (circle/square/diamond/triangle), NOT color
- **2.5-Second Refresh Cycle:** Computer updates drum every 2.5s (historically accurate)
- **Phosphor Persistence:** Purple flash → orange afterglow (2-3 second decay)

**DO NOT:**
- Change `drawTracksOnPersistence()` to run every frame (breaks historical accuracy)
- Remove `updateTrackData()` method (required for refresh cycle)
- Change `refreshInterval` without documenting historical justification
- Add color coding to track symbology (must be monochrome P14 phosphor)

---

## 🔧 Development Workflow

### Branch Strategy
1. Create feature branch from `main`: `git checkout -b feature/your-feature-name`
2. Make changes with frequent commits
3. Run tests locally before pushing
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open Pull Request on GitHub

### Commit Message Format
Use conventional commits:
```
feat: add scenario event system
fix: correct light gun canvas coordinates
docs: update ARCHITECTURE.md with drum I/O
refactor: extract track rendering to separate module
test: add unit tests for CPU indexed addressing
perf: cache JSON serialization with @rx.var(cache=True)
```

### Pull Request Checklist
- [ ] Tests added/updated and passing
- [ ] Manual testing completed (checklist above)
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (if user-facing change)
- [ ] No merge conflicts with `main`
- [ ] Code follows style guidelines
- [ ] Design invariants preserved (mode-free UI, P14 monochrome, etc.)

---

## 🐛 Reporting Issues

### Bug Reports
Include:
- **Environment:** OS, Python version, UV version
- **Steps to Reproduce:** Exact sequence to trigger bug
- **Expected Behavior:** What should happen
- **Actual Behavior:** What actually happens
- **Screenshots:** If visual bug
- **Console Logs:** Browser console (F12) and terminal output

### Feature Requests
Include:
- **Use Case:** Why is this feature needed?
- **Proposed Solution:** How should it work?
- **Alternatives Considered:** Other approaches you've thought of
- **Persona:** Which persona benefits (Ada/Grace/Sam)?
- **Historical Accuracy:** Does this align with SAGE authenticity?

---

## 📚 Documentation Guidelines

### When to Update Docs
- **New Feature:** Update README.md and relevant docs/ files
- **API Change:** Update components_v2/README.md
- **Design Invariant:** Update agents.md
- **User-Facing Change:** Update CHANGELOG.md
- **Session Work:** Save to docs/archive/completed_sessions/

### Documentation Files
- **README.md** - Main entry, feature showcase
- **QUICKSTART.md** - Fast setup guide
- **PROJECT_STATUS.md** - Current status snapshot
- **agents.md** - Developer patterns & critical gotchas
- **docs/ARCHITECTURE.md** - System structure
- **docs/DESIGN.md** - Design philosophy
- **docs/USER_GUIDE.md** - Comprehensive user manual
- **CHANGELOG.md** - Version history

---

## 🎯 Priority Areas for Contribution

### High Priority
1. **Testing Infrastructure** (CRITICAL - currently minimal tests)
   - Unit tests for CPU core, drum I/O, light gun
   - Simulation tests for scenarios, physics
   - Design language contract tests

2. **Cross-Browser Testing**
   - Firefox, Safari, Edge compatibility
   - Mobile/touch support for light gun

3. **Accessibility**
   - Keyboard navigation
   - Screen reader support
   - WCAG compliance

### Medium Priority
4. **Historical Scenarios**
   - Cuban Missile Crisis
   - Berlin Airlift
   - Real historical incidents

5. **Feature Enhancements**
   - Multi-player support (multiple consoles)
   - SAGE command language interpreter
   - Weather effects (rain clutter, storms)

6. **Performance**
   - Profiling with 100+ tracks
   - WebGL shader optimizations
   - Lazy loading for large scenarios

---

## 🤝 Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Help newcomers learn
- Focus on the code, not the person
- Keep discussions on-topic

---

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Security:** Email maintainer directly (do not open public issue)
- **Design Decisions:** Review docs/DESIGN.md and agents.md first

---

## 🏆 Recognition

Contributors will be acknowledged in:
- README.md acknowledgments section
- CHANGELOG.md for significant features
- GitHub contributor graph

Thank you for helping preserve and educate about the AN/FSQ-7 SAGE computer! 🎯✨
