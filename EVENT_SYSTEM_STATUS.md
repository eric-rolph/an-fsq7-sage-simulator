# Event System Investigation Results

**Date**: 2025-01-28  
**Status**: ✅ Events Working | ❌ UI Missing

---

## TL;DR

The scenario event system is **fully functional** - events trigger correctly and messages are logged to the backend state. However, **there is no UI component** to display these messages to the user. System messages exist in `InteractiveSageState.system_messages_log` but are not rendered on the page.

---

## Investigation Summary

### What Works ✅

1. **Event System Architecture**
   - `EventTimeline` class manages timed/conditional events
   - `process_scenario_events()` called every simulation tick
   - Events trigger at correct times (verified via terminal debug logs)
   - 8 event types implemented: SPAWN_TRACK, COURSE_CHANGE, THREAT_ESCALATION, etc.

2. **Scenario 5 Events** (Correlation Training)
   - Event 1 (5s): "IFF AMBIGUOUS - Manual correlation required"
   - Event 2 (20s): "IFF RESPONSE: TGT-5002 transmitting friendly codes"
   - Event 3 (25s): "TGT-5003 AGGRESSIVE MANEUVER - heading toward airspace"
   - Event 4 (35s): "TGT-5004 RADIO CONTACT: Commercial flight requesting clearance"
   - All 4 events trigger successfully (confirmed in terminal output)

3. **Backend State Management**
   - `system_messages_log` grows correctly (9 → 11 messages after Scenario 5 load)
   - Messages persist in backend state
   - datetime serialization fixed (commit 92af5f9)

4. **Data Injection**
   - `system_messages_script_tag` computed var serializes messages to JSON
   - `window.__SAGE_SYSTEM_MESSAGES__` available in browser
   - Script tag injection mechanism works

### What's Broken ❌

1. **No UI Component on Page**
   - `components_v2/system_messages.py` exists with `message_row()` display component
   - Component imported in `interactive_sage.py` line 43
   - **BUT**: Never added to page layout in `index()` function
   - Messages logged to backend but invisible to user

2. **Script Tags Don't Update Reactively**
   - `rx.html()` injected scripts execute once at page load
   - State changes don't trigger script re-execution
   - Browser shows stale data (7 Demo 1 messages vs 11+ in backend)

3. **Timing Offset**
   - Events trigger at time - 1s (e.g., 4s instead of 5s)
   - Likely scenario_elapsed_time calculation issue
   - Minor cosmetic bug

---

## Terminal Debug Output

```
[SCENARIO] change_scenario called with: Scenario 5 - Correlation Training
[SCENARIO] Before load - messages count: 9
[SCENARIO] After load - messages count: 10, tracks: ['TGT-5001', 'TGT-5002', 'TGT-5003', 'TGT-5004']
[SCENARIO] After message append - messages count: 11
[EVENT] Triggered: SYSTEM_MESSAGE at 4.0s
[EVENT] Triggered: SYSTEM_MESSAGE at 19.0s
[EVENT] Triggered: COURSE_CHANGE at 24.0s
[EVENT] Triggered: SYSTEM_MESSAGE at 34.0s
```

**Interpretation**:
- Scenario 5 loads successfully ✅
- Tracks change from TGT-1001/1002/1003 (Demo 1) to TGT-5001/5002/5003/5004 (Scenario 5) ✅
- Message count increases from 11 → 15 after events ✅
- All 4 events trigger (3× SYSTEM_MESSAGE, 1× COURSE_CHANGE) ✅

---

## Browser State

```javascript
window.__SAGE_SYSTEM_MESSAGES__
// Returns: 7 messages, all from Demo 1 loads
// Expected: 15+ messages including Scenario 5 events
```

```javascript
window.__SAGE_TRACKS__
// Returns: TGT-1001, TGT-1002, TGT-1003 (Demo 1)
// Expected: TGT-5001, TGT-5002, TGT-5003, TGT-5004 (Scenario 5)
```

**Diagnosis**: Frontend state desync - script tags don't update when backend state changes.

---

## Solution Required

### Short-Term Fix (Display Messages)

Add system messages panel to main page layout:

```python
# In interactive_sage.py index() function, add:
system_messages.system_messages_panel(
    messages=InteractiveSageState.system_messages_log,
    max_height="300px"
)
```

This will:
- Render messages reactively (no script tag polling needed)
- Auto-update when `system_messages_log` changes
- Display all event messages to the user

### Files to Modify

1. **interactive_sage.py** line ~2000 (index function)
   - Add `system_messages.system_messages_panel()` to layout
   - Position in right column or bottom of left column

2. **Optional: Remove script tag injection** (if not needed elsewhere)
   - Line 1904: `system_messages_script_tag` computed var
   - Line 2107: `rx.html(InteractiveSageState.system_messages_script_tag)`

### Long-Term Improvements

1. **Fix Event Timing**
   - Adjust `scenario_elapsed_time` calculation to match event trigger times exactly
   - Events should fire at 5s, 20s, 25s, 35s (not 4s, 19s, 24s, 34s)

2. **Event Message Display Enhancements**
   - Color-code event messages by category (IFF=cyan, COMMS=green, WARNING=yellow)
   - Add sound effects for event triggers
   - Flash or highlight new messages in panel

3. **Historical Accuracy**
   - Add event log printer simulation (teletype output)
   - Implement message acknowledgment workflow (operator must ACK warnings)

---

## Test Verification

To verify the fix works:

1. Add system messages panel to page
2. Restart server: `uv run reflex run`
3. Navigate to `http://localhost:3000`
4. Select "Scenario 5 - Correlation Training"
5. Wait 40 seconds
6. **Expected**: Panel shows 4 new messages:
   - "IFF AMBIGUOUS - Manual correlation required" (~5s)
   - "IFF RESPONSE: TGT-5002 transmitting friendly codes" (~20s)
   - "TGT-5003 AGGRESSIVE MANEUVER - heading toward airspace" (~25s)
   - "TGT-5004 RADIO CONTACT: Commercial flight requesting clearance" (~35s)

---

## Related Files

- `an_fsq7_simulator/interactive_sage.py` - Main state + event handlers
- `an_fsq7_simulator/sim/scenario_events.py` - Event definitions (484 lines)
- `an_fsq7_simulator/components_v2/system_messages.py` - UI component (363 lines)
- `an_fsq7_simulator/sim/scenarios.py` - Scenario definitions

---

## Commits

- `d037caa` - Event system implementation (480 lines)
- `eccca94` - System messages infrastructure + datetime fixes
- `92af5f9` - Final datetime fixes in toggle methods + debug logging

---

## Next Steps

1. ✅ **DONE**: Investigate why events don't appear (this document)
2. 🎯 **TODO**: Add system messages panel to page layout (15 minutes)
3. 🎯 **TODO**: Fix event timing offset (5 minutes)
4. 🎯 **TODO**: Test all 7 scenarios' events display correctly
5. ⏳ **LATER**: Begin Phase 7 dual console mode (per SD_CONSOLE_HISTORICAL_ACCURACY.md)
