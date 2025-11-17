"""
Test script to verify tabular display feature generation integration.

This tests that update_track_display_features() correctly generates
features A/B/C/D for tracks with various properties.
"""

from an_fsq7_simulator import state_model

# Test Case 1: High-altitude hostile aircraft
track1 = state_model.Track(
    id="TGT-1001",
    x=0.25, y=0.25,
    vx=0.01, vy=0.01,
    altitude=35000,
    speed=520,
    heading=315,
    track_type="aircraft",
    threat_level="HIGH",
    time_detected=0.0
)

print("=== Test Case 1: High-altitude hostile ===")
print(f"Before feature generation:")
print(f"  feature_a: {track1.feature_a}")
print(f"  feature_b: {track1.feature_b}")
print(f"  feature_c: {track1.feature_c}")
print(f"  feature_d: {track1.feature_d}")

state_model.update_track_display_features(track1)

print(f"\nAfter feature generation:")
print(f"  feature_a: '{track1.feature_a}' (expected: 4 chars)")
print(f"  feature_b: '{track1.feature_b}' (expected: altitude + speed)")
print(f"  feature_c: '{track1.feature_c}' (expected: classification)")
print(f"  feature_d: '{track1.feature_d}' (expected: heading quadrant)")

# Test Case 2: Medium-altitude friendly aircraft
track2 = state_model.Track(
    id="FRD-0042",
    x=0.75, y=0.75,
    vx=-0.005, vy=-0.005,
    altitude=22000,
    speed=380,
    heading=135,
    track_type="friendly",
    threat_level="LOW",
    time_detected=10.0
)

print("\n=== Test Case 2: Medium-altitude friendly ===")
state_model.update_track_display_features(track2)
print(f"  feature_a: '{track2.feature_a}'")
print(f"  feature_b: '{track2.feature_b}'")
print(f"  feature_c: '{track2.feature_c}'")
print(f"  feature_d: '{track2.feature_d}'")

# Test Case 3: Low-altitude missile
track3 = state_model.Track(
    id="MSL-9999",
    x=0.5,
    y=0.5,
    vx=0.02,
    vy=0.0,
    altitude=5000,
    speed=1200,
    heading=90,
    track_type="missile",
    threat_level="HIGH",
    time_detected=20.0
)

print("\n=== Test Case 3: Low-altitude missile ===")
state_model.update_track_display_features(track3)
print(f"  feature_a: '{track3.feature_a}'")
print(f"  feature_b: '{track3.feature_b}'")
print(f"  feature_c: '{track3.feature_c}'")
print(f"  feature_d: '{track3.feature_d}'")

# Validation checks
print("\n=== Validation ===")
errors = []

if not track1.feature_a or len(track1.feature_a) != 4:
    errors.append(f"Track 1 feature_a wrong length: '{track1.feature_a}'")
if not track1.feature_b or len(track1.feature_b) != 4:
    errors.append(f"Track 1 feature_b wrong length: '{track1.feature_b}'")
if not track1.feature_c or len(track1.feature_c) != 4:
    errors.append(f"Track 1 feature_c wrong length: '{track1.feature_c}'")
if not track1.feature_d or len(track1.feature_d) != 2:
    errors.append(f"Track 1 feature_d wrong length: '{track1.feature_d}'")

if not track2.feature_a or len(track2.feature_a) != 4:
    errors.append(f"Track 2 feature_a wrong length: '{track2.feature_a}'")
if not track3.feature_a or len(track3.feature_a) != 4:
    errors.append(f"Track 3 feature_a wrong length: '{track3.feature_a}'")

if errors:
    print(f"❌ FAILED - {len(errors)} errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ All validation checks passed!")
    print(f"\n✓ Feature generation working correctly")
    print(f"✓ All features have correct lengths (A=4, B=4, C=4, D=2)")
    print(f"✓ Ready for integration with CRT renderer")
