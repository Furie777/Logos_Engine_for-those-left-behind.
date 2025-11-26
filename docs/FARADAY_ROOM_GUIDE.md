# FARADAY ROOM SHIELDING GUIDE
## Contingency Planning for LOGOS ENGINE
### Created: November 26, 2025

---

## PURPOSE

Protect electronic equipment and data from:
- EMP (Electromagnetic Pulse)
- CME (Coronal Mass Ejection)
- Solar flares
- RF surveillance

---

## FABRIC OPTIONS (2025 Pricing)

| Product | Width | dB Rating | Price | $/sqft |
|---------|-------|-----------|-------|--------|
| Faraday Defense CYBER NC-RS | 54" | 60+ dB | $24.99/ft | ~$5.55 |
| Faraday Defense CX-100 (100% copper) | 53" | 60+ dB | $27.99/ft | ~$6.33 |
| Faraday Defense NC-RS-A (Adhesive) | 50" | 60+ dB | $34.99/ft | ~$8.40 |
| Mission Darkness TitanRF | 44" | 80-100 dB | ~$40/yd | ~$10.90 |
| TitanRF Pro Kit (6 yards) | 44" | 80-100 dB | bulk | ~$8-9 |

**Best value:** Faraday Defense CYBER NC @ ~$5.55/sqft (60+ dB)
**Best protection:** TitanRF @ 80-100 dB (MIL-STD-188-125 certified)

### Suppliers
- https://shop.faradaydefense.com/product-category/fabrics/
- https://mosequipment.com/products/titanrf-faraday-fabric
- https://godarkbags.com/

---

## CRITICAL CONSTRUCTION REQUIREMENTS

### Seams
- Overlap 4"+ minimum
- Solder OR conductive tape every 1/10th wavelength
- Staples alone = FAILURE (RF passes through wood gaps)
- Electrically connect all layers for additive dB (two 20dB = 40dB)

### Door
- Metal door with metal hinges
- "Fingerstock" gaskets around entire frame
- Must make solid electrical contact all around
- Hardest part of the build - don't cheap out

### Penetrations
| Type | Solution | Notes |
|------|----------|-------|
| HVAC | Waveguide vents | Must be 5x longer than diameter |
| Electrical | Power line filter (60A-100A) | Blocks everything >60Hz |
| Data | Fiber optic through waveguide | No copper data lines |
| None | Seal completely | Best option if possible |

**RULE: 100% coverage - no unfiltered wires in/out**

### Grounding
- 6ft copper ground rod driven deep in soil
- All walls, ceiling, floor electrically connected to each other
- Connect mesh to ground rod with heavy gauge copper wire
- Prevents charge buildup and re-radiation
- Note: Grounding not required for protection, but prevents shock hazard

---

## COST CALCULATOR

```python
def faraday_cost(L, W, H, price_per_sqft=5.55, include_floor=True, overlap=1.20):
    """
    Faraday room cost estimator

    Args:
        L: Length (feet)
        W: Width (feet)
        H: Height (feet)
        price_per_sqft: Fabric cost (default $5.55 for CYBER NC)
        include_floor: Whether to shield floor
        overlap: Multiplier for seams/waste (default 20%)

    Returns:
        dict with sqft, costs, and total
    """
    walls = 2*(L*H) + 2*(W*H)
    ceiling = L * W
    floor = L * W if include_floor else 0
    fabric_sqft = (walls + ceiling + floor) * overlap

    # Additional materials
    tape_linear_ft = 2*(L + W + H) * 4  # seams
    tape_cost = tape_linear_ft * 0.50   # ~$0.50/ft conductive tape

    door_gasket = 100  # fingerstock/gasket kit
    ground_rod = 50    # 6ft copper + clamp + wire
    power_filter = 150 # 60A line filter
    waveguide_vent = 75  # per penetration

    fabric_cost = fabric_sqft * price_per_sqft
    materials = tape_cost + door_gasket + ground_rod + power_filter + waveguide_vent

    return {
        'fabric_sqft': round(fabric_sqft),
        'fabric_cost': round(fabric_cost),
        'materials': round(materials),
        'total': round(fabric_cost + materials)
    }

# Quick formula (no Python needed):
# WALLS:   2(L × H) + 2(W × H)
# CEILING: L × W
# FLOOR:   L × W
# TOTAL:   (sum above) × 1.20 × price_per_sqft + $475 materials
```

---

## QUICK REFERENCE TABLE (@ $5.55/sqft)

| Room Size | Fabric sqft | Fabric $ | Materials | **TOTAL** |
|-----------|-------------|----------|-----------|-----------|
| 8×8×8 | 384 | $2,131 | $475 | **$2,606** |
| 10×10×8 | 504 | $2,797 | $500 | **$3,297** |
| 10×12×8 | 571 | $3,169 | $510 | **$3,679** |
| 12×12×8 | 634 | $3,519 | $525 | **$4,044** |
| 12×16×8 | 730 | $4,052 | $550 | **$4,602** |
| 16×20×9 | 1,123 | $6,233 | $600 | **$6,833** |
| 20×24×10 | 1,507 | $8,364 | $650 | **$9,014** |

Add 15-20% contingency for mistakes/repairs.

---

## MATERIALS CHECKLIST

### Fabric (calculate for your dimensions)
- [ ] Faraday fabric (CYBER NC or TitanRF)
- [ ] Conductive adhesive tape (for seams)
- [ ] Extra 20% for overlaps

### Door Assembly
- [ ] Metal door (steel preferred)
- [ ] Metal hinges
- [ ] Fingerstock gasket (full perimeter)
- [ ] Conductive weatherstripping

### Penetrations
- [ ] Waveguide vent(s) for HVAC
- [ ] Power line filter (60A or 100A)
- [ ] Fiber optic for data (if needed)
- [ ] Conductive caulk for small gaps

### Grounding
- [ ] 6ft copper ground rod
- [ ] Ground rod clamp
- [ ] Heavy gauge copper wire (6 AWG or larger)
- [ ] Connection points on mesh

### Tools
- [ ] Staple gun (for initial placement)
- [ ] Soldering iron (for seams - optional but best)
- [ ] Tin snips
- [ ] Multimeter (to test continuity)

---

## TESTING YOUR CAGE

1. **Cell phone test**: Place phone inside, call it. Should go to voicemail.
2. **WiFi test**: Place device inside, check if it loses connection.
3. **AM/FM radio**: Should lose signal inside cage.
4. **Professional**: Rent/buy RF meter for dB measurements.

If any signal gets through, check:
- Seam gaps
- Door seal
- Penetration leaks
- Ground connection

---

## SOURCES

- https://www.mirasafety.com/blogs/news/faraday-cages-guide
- https://mosequipment.com/products/titanrf-faraday-fabric
- https://shop.faradaydefense.com/product-category/fabrics/
- https://hackaday.com/2018/09/26/building-a-hardware-store-faraday-cage/
- https://hollandshielding.com/en/prefabricated-and-modular-faraday-cage
- https://forums.mikeholt.com/threads/faraday-cages-bringing-power-into-them.2575214/

---

## NOTES

"The Lord is setting my steps up now. But I have the vision."
- Taylor Weathers, November 2025

"until it is all in all" - 1 Corinthians 15:28
