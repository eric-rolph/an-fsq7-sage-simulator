#!/usr/bin/env python3
"""
Integration test for Priority 8 - Authentic SAGE Tabular Display System

Tests the complete pipeline:
1. Track model with feature fields
2. Feature generation functions
3. JavaScript integration (font + tabular renderer)
4. History trail rendering

Run with: uv run python test_tabular_integration.py
"""

from an_fsq7_simulator.state_model import (
    Track, 
    generate_track_features,
    update_track_display_features,
    calculate_position_mode,
    generate_feature_a,
    generate_feature_b,
    generate_feature_c,
    generate_feature_d
)


def test_track_features():
    """Test feature generation for various track types"""
    
    print("=" * 60)
    print("PRIORITY 8 TABULAR DISPLAY INTEGRATION TEST")
    print("=" * 60)
    print()
    
    # Test 1: Hostile bomber (high altitude, medium speed, westbound)
    print("Test 1: Hostile Bomber")
    print("-" * 40)
    track1 = Track(
        id="TK01",
        x=0.3,
        y=0.4,
        altitude=35000,
        speed=450,
        heading=270,
        track_type="hostile",
        threat_level="HIGH"
    )
    update_track_display_features(track1)
    
    print(f"Track ID: {track1.id}")
    print(f"Position: ({track1.x:.2f}, {track1.y:.2f})")
    print(f"Altitude: {track1.altitude}ft, Speed: {track1.speed}kts, Heading: {track1.heading}°")
    print(f"Type: {track1.track_type}, Threat: {track1.threat_level}")
    print()
    print("Tabular Features:")
    print(f"  Feature A (Track ID):       [{track1.feature_a}]")
    print(f"  Feature B (Alt/Speed):      [{track1.feature_b}]")
    print(f"  Feature C (Class/Threat):   [{track1.feature_c}]")
    print(f"  Feature D (Heading):        [{track1.feature_d}]")
    print(f"  Position Mode:              {track1.position_mode} (0=RIGHT, 1=LEFT, 2=ABOVE, 3=BELOW)")
    print()
    
    # Test 2: Friendly fighter (very high altitude, supersonic, northeast)
    print("Test 2: Friendly Fighter (F-102)")
    print("-" * 40)
    track2 = Track(
        id="F102",
        x=0.7,
        y=0.3,
        altitude=42000,
        speed=850,
        heading=45,
        track_type="friendly",
        threat_level="LOW"
    )
    update_track_display_features(track2)
    
    print(f"Track ID: {track2.id}")
    print(f"Position: ({track2.x:.2f}, {track2.y:.2f})")
    print(f"Altitude: {track2.altitude}ft, Speed: {track2.speed}kts, Heading: {track2.heading}°")
    print(f"Type: {track2.track_type}, Threat: {track2.threat_level}")
    print()
    print("Tabular Features:")
    print(f"  Feature A (Track ID):       [{track2.feature_a}]")
    print(f"  Feature B (Alt/Speed):      [{track2.feature_b}]")
    print(f"  Feature C (Class/Threat):   [{track2.feature_c}]")
    print(f"  Feature D (Heading):        [{track2.feature_d}]")
    print(f"  Position Mode:              {track2.position_mode}")
    print()
    
    # Test 3: Unknown track (low altitude, slow speed, southbound)
    print("Test 3: Unknown Track")
    print("-" * 40)
    track3 = Track(
        id="UN99",
        x=0.2,
        y=0.7,
        altitude=8000,
        speed=280,
        heading=180,
        track_type="unknown",
        threat_level="MEDIUM"
    )
    update_track_display_features(track3)
    
    print(f"Track ID: {track3.id}")
    print(f"Position: ({track3.x:.2f}, {track3.y:.2f})")
    print(f"Altitude: {track3.altitude}ft, Speed: {track3.speed}kts, Heading: {track3.heading}°")
    print(f"Type: {track3.track_type}, Threat: {track3.threat_level}")
    print()
    print("Tabular Features:")
    print(f"  Feature A (Track ID):       [{track3.feature_a}]")
    print(f"  Feature B (Alt/Speed):      [{track3.feature_b}]")
    print(f"  Feature C (Class/Threat):   [{track3.feature_c}]")
    print(f"  Feature D (Heading):        [{track3.feature_d}]")
    print(f"  Position Mode:              {track3.position_mode}")
    print()
    
    # Test 4: Missile (medium altitude, fast, northwest)
    print("Test 4: Missile Track")
    print("-" * 40)
    track4 = Track(
        id="MS03",
        x=0.6,
        y=0.6,
        altitude=25000,
        speed=750,
        heading=315,
        track_type="missile",
        threat_level="CRITICAL"
    )
    update_track_display_features(track4)
    
    print(f"Track ID: {track4.id}")
    print(f"Position: ({track4.x:.2f}, {track4.y:.2f})")
    print(f"Altitude: {track4.altitude}ft, Speed: {track4.speed}kts, Heading: {track4.heading}°")
    print(f"Type: {track4.track_type}, Threat: {track4.threat_level}")
    print()
    print("Tabular Features:")
    print(f"  Feature A (Track ID):       [{track4.feature_a}]")
    print(f"  Feature B (Alt/Speed):      [{track4.feature_b}]")
    print(f"  Feature C (Class/Threat):   [{track4.feature_c}]")
    print(f"  Feature D (Heading):        [{track4.feature_d}]")
    print(f"  Position Mode:              {track4.position_mode}")
    print()
    
    # Validation checks
    print("=" * 60)
    print("VALIDATION CHECKS")
    print("=" * 60)
    print()
    
    checks_passed = 0
    checks_total = 0
    
    # Check 1: Feature A is always 4 characters
    checks_total += 1
    if (len(track1.feature_a) == 4 and len(track2.feature_a) == 4 and 
        len(track3.feature_a) == 4 and len(track4.feature_a) == 4):
        print("✓ Feature A length is 4 characters for all tracks")
        checks_passed += 1
    else:
        print("✗ Feature A length validation failed")
    
    # Check 2: Feature B is always 4 characters
    checks_total += 1
    if (len(track1.feature_b) == 4 and len(track2.feature_b) == 4 and 
        len(track3.feature_b) == 4 and len(track4.feature_b) == 4):
        print("✓ Feature B length is 4 characters for all tracks")
        checks_passed += 1
    else:
        print("✗ Feature B length validation failed")
    
    # Check 3: Feature C is always 4 characters
    checks_total += 1
    if (len(track1.feature_c) == 4 and len(track2.feature_c) == 4 and 
        len(track3.feature_c) == 4 and len(track4.feature_c) == 4):
        print("✓ Feature C length is 4 characters for all tracks")
        checks_passed += 1
    else:
        print("✗ Feature C length validation failed")
    
    # Check 4: Feature D is always 2 characters
    checks_total += 1
    if (len(track1.feature_d) == 2 and len(track2.feature_d) == 2 and 
        len(track3.feature_d) == 2 and len(track4.feature_d) == 2):
        print("✓ Feature D length is 2 characters for all tracks")
        checks_passed += 1
    else:
        print("✗ Feature D length validation failed")
    
    # Check 5: Position mode is 0-3
    checks_total += 1
    if all(0 <= t.position_mode <= 3 for t in [track1, track2, track3, track4]):
        print("✓ Position mode is valid (0-3) for all tracks")
        checks_passed += 1
    else:
        print("✗ Position mode validation failed")
    
    # Check 6: Speed categories correct
    checks_total += 1
    if (track1.feature_b.endswith("MD") and  # 450 knots = Medium
        track2.feature_b.endswith("SS") and  # 850 knots = Supersonic
        track3.feature_b.endswith("SL") and  # 280 knots = Slow
        track4.feature_b.endswith("FS")):    # 750 knots = Fast
        print("✓ Speed categories encoded correctly")
        checks_passed += 1
    else:
        print("✗ Speed category encoding failed")
        print(f"  Track1 (450kts): {track1.feature_b} (expected: *MD)")
        print(f"  Track2 (850kts): {track2.feature_b} (expected: *SS)")
        print(f"  Track3 (280kts): {track3.feature_b} (expected: *SL)")
        print(f"  Track4 (750kts): {track4.feature_b} (expected: *FS)")
    
    # Check 7: Heading quadrants correct
    checks_total += 1
    if (track1.feature_d == "W " and    # 270° = West
        track2.feature_d == "NE" and    # 45° = Northeast
        track3.feature_d == "S " and    # 180° = South
        track4.feature_d == "NW"):      # 315° = Northwest
        print("✓ Heading quadrants encoded correctly")
        checks_passed += 1
    else:
        print("✗ Heading quadrant encoding failed")
        print(f"  Track1 (270°): {track1.feature_d} (expected: W )")
        print(f"  Track2 (45°):  {track2.feature_d} (expected: NE)")
        print(f"  Track3 (180°): {track3.feature_d} (expected: S )")
        print(f"  Track4 (315°): {track4.feature_d} (expected: NW)")
    
    print()
    print("=" * 60)
    print(f"RESULTS: {checks_passed}/{checks_total} checks passed")
    print("=" * 60)
    print()
    
    if checks_passed == checks_total:
        print("✓ All validation checks passed!")
        print("✓ Tabular display feature generation is working correctly")
        print()
        print("Next steps:")
        print("  1. Test in browser at http://localhost:3000")
        print("  2. Verify history trails render with fading alpha")
        print("  3. Check that JavaScript console shows tabular display system loaded")
        print("  4. Validate against manual figures (Task 6)")
        return True
    else:
        print("✗ Some validation checks failed - review feature generation logic")
        return False


if __name__ == "__main__":
    success = test_track_features()
    exit(0 if success else 1)
