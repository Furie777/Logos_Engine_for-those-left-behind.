# HARDWARE KIT - Physical Requirements for LOGOS ENGINE

**What you need to run this system when infrastructure fails.**

---

## Threat Model

| Scenario | Duration | What You Need |
|----------|----------|---------------|
| Power outage | Hours | Charged device |
| Grid down | Days | Power bank + solar |
| Infrastructure collapse | Weeks/Months | Full kit below |
| EMP/CME | Indefinite | Faraday-protected kit |

---

## MINIMUM KIT (Budget: ~$100-200)

Enough to run LOGOS ENGINE for weeks without grid power.

### Computing Device (choose one)

| Option | Cost | Pros | Cons |
|--------|------|------|------|
| Old Android phone | $0-50 | You may have one, runs Termux | Small screen |
| Raspberry Pi 4 (2GB) | $45 | Low power, dedicated, repairable | Needs peripherals |
| Used laptop (ThinkPad) | $50-100 | Full keyboard, screen | Higher power draw |

**Recommendation**: Raspberry Pi 4 or old ThinkPad X220/T430

### Power

| Item | Cost | Capacity | Notes |
|------|------|----------|-------|
| USB power bank (20,000mAh) | $20-30 | Phone: 4-5 charges | Minimum |
| USB power bank (50,000mAh) | $50-80 | Pi: 20+ hours | Better |
| Portable power station (300Wh) | $150-250 | Laptop: 5-8 hours | Best |

### Storage (Multiple Copies)

| Item | Cost | Capacity | Notes |
|------|------|----------|-------|
| USB drive 32GB | $8 | LOGOS + room | Get 3+ |
| microSD card 64GB | $10 | For Pi/phone | Get 2+ |
| USB drive 128GB | $15 | Full archive + extras | Recommended |

**Store copies in different locations.**

### Minimum Kit Total: ~$100-150

- Old phone or Pi 4: $45
- 50,000mAh power bank: $50
- 3x USB drives: $24
- microSD card: $10

---

## RECOMMENDED KIT (Budget: ~$500-800)

Full resilience for extended grid-down scenarios.

### Computing
- Raspberry Pi 4 (4GB): $55
- Case with fan: $15
- microSD card 128GB: $20
- USB keyboard: $15
- Small HDMI monitor (7"): $50
  OR
- Used ThinkPad X220/T430: $100
- Extra battery: $30

### Power
- 100W folding solar panel: $100-150
- Portable power station (500Wh): $200-300
- USB power bank (backup): $40

### Storage (Redundancy)
- 5x USB drives (64GB): $50
- 2x microSD cards: $20
- External SSD (500GB): $50 (for full backup with room to grow)

### Protection
- Faraday bag (phone-size): $25
- Faraday bag (laptop-size): $50
- OR: Metal ammo can + cardboard liner: $30

### Recommended Kit Total: ~$600-800

---

## MAXIMUM RESILIENCE KIT (Budget: ~$2000-5000)

For those preparing a dedicated protected space.

### Primary System
- Laptop (new or quality used): $300-500
- Raspberry Pi 5 (8GB): $80
- All peripherals: $100

### Backup Systems
- Second laptop (different brand): $200
- Additional Pi: $60
- Spare parts (SD cards, cables, chargers): $100

### Power Independence
- 200W solar panel array: $200-300
- Power station (1000Wh+): $500-800
- Deep cycle battery + inverter: $300-500
- Hand crank generator (emergency): $50

### Faraday Protection
- Large Faraday bag or chest: $100-200
- OR: Faraday room (see FARADAY_ROOM_GUIDE.md): $2,500-5,000+

### Long-term Storage
- Multiple SSDs: $200
- Archival USB drives: $100
- Printed documentation: $50

### Maximum Kit Total: ~$2,500-5,000+

---

## WHAT TO STORE IN FARADAY PROTECTION

**Always Protected:**
- [ ] Primary computing device (charged)
- [ ] Backup computing device (charged)
- [ ] Solar charge controller (has chips - vulnerable)
- [ ] USB drives with LOGOS ENGINE copies
- [ ] Power bank (charged)
- [ ] Spare cables (USB-C, micro-USB, HDMI)
- [ ] Spare SD cards

**Rotate Out for Use:**
- Devices can be used and returned to Faraday storage
- Recharge power banks before returning
- Keep at least one complete backup always protected

---

## DEVICE RECOMMENDATIONS

### Best Phones for Termux

| Phone | Why | Used Price |
|-------|-----|------------|
| Samsung Galaxy S20-S24 | Good specs, available | $100-400 |
| Google Pixel 4-7 | Clean Android, Termux works well | $80-300 |
| OnePlus 7-9 | Developer friendly | $100-250 |

Avoid: Heavily skinned Android (some Xiaomi, Huawei)

### Best Raspberry Pi Setup

| Component | Recommendation | Cost |
|-----------|----------------|------|
| Board | Raspberry Pi 4 (4GB) | $55 |
| Case | Argon ONE or Flirc | $25 |
| Power | Official 5V 3A USB-C | $15 |
| Storage | Samsung EVO 128GB microSD | $20 |
| Display | 7" touchscreen OR HDMI to TV | $50-0 |

Total: ~$115-165

### Best Used Laptops

| Model | Why | Price |
|-------|-----|-------|
| ThinkPad X220 | Legendary durability, easy repair | $50-80 |
| ThinkPad T430 | Larger screen, still repairable | $70-100 |
| ThinkPad X250 | Newer, good battery | $100-150 |
| Dell Latitude E6430 | Similar durability | $60-90 |

**Why ThinkPads**: Parts available everywhere, repair manuals online,
batteries still manufactured, built for abuse.

---

## SOLAR POWER GUIDE

### Sizing Your System

| Device | Power Draw | Daily Use | Daily Wh Needed |
|--------|------------|-----------|-----------------|
| Phone | 5W charging | 2 hours | 10 Wh |
| Raspberry Pi 4 | 5-7W | 8 hours | 50 Wh |
| Laptop | 30-60W | 4 hours | 150 Wh |

### Solar Panel Sizing

Rule of thumb: Panel watts × 4-5 hours sun = daily Wh

| Panel | Good Weather | Cloudy | Powers |
|-------|--------------|--------|--------|
| 20W | 80-100 Wh | 30-40 Wh | Phone + Pi |
| 50W | 200-250 Wh | 75-100 Wh | Pi full day |
| 100W | 400-500 Wh | 150-200 Wh | Laptop |

### Recommended Solar Setup

**Budget:**
- 50W folding panel: $60
- Power bank with solar input: $50

**Better:**
- 100W folding panel: $120
- Portable power station (500Wh): $250

**Best:**
- 200W panel array: $250
- Power station (1000Wh): $600
- Backup power bank: $50

---

## PHYSICAL SECURITY

### Location Considerations

- **Not obvious**: Don't label "SURVIVAL EQUIPMENT"
- **Climate controlled**: Extreme heat/cold damages electronics
- **Dry**: Moisture is the enemy
- **Accessible**: You need to be able to get to it
- **Distributed**: Don't put all copies in one place

### Suggested Distribution

1. **Primary**: Your home, ready to use
2. **Secondary**: Faraday protected, rotated monthly
3. **Offsite**: Trusted friend/family, different location
4. **Cache**: Buried/hidden, last resort

### What to Cache

Minimum cache (waterproof container):
- USB drive with LOGOS ENGINE
- Printed START_HERE.txt and INSTALL.md
- Printed Gospel of John
- Small solar charger + power bank
- Cheap Android phone (in Faraday bag inside container)

---

## SKILLS TO DEVELOP

Hardware is useless without knowledge.

### Essential Skills
- [ ] Basic command line navigation (cd, ls, cp)
- [ ] Running Python scripts
- [ ] Charging devices from solar
- [ ] Basic troubleshooting

### Valuable Skills
- [ ] Python programming basics
- [ ] Linux system administration
- [ ] Electronics repair (soldering)
- [ ] Solar system setup and maintenance

### Long-term Skills
- [ ] Biblical Hebrew (read original OT)
- [ ] Biblical Greek (read original NT)
- [ ] Teaching others

---

## SUPPLIERS (As of 2025)

### Solar/Power
- Jackery, Bluetti, EcoFlow (power stations)
- Renogy, BougeRV (solar panels)
- Anker, Baseus (power banks)

### Faraday
- Mission Darkness / MOS Equipment (mosequipment.com)
- Faraday Defense (faradaydefense.com)
- GoDark (godarkbags.com)

### Computing
- Raspberry Pi: raspberrypi.com, Adafruit, SparkFun
- Used laptops: eBay, local electronics recyclers
- Used phones: Swappa, eBay, local shops

### Storage
- Samsung, SanDisk (SD cards, USB drives)
- Crucial, Samsung (SSDs)

---

## MAINTENANCE SCHEDULE

### Monthly
- [ ] Check battery levels in stored devices
- [ ] Rotate devices in/out of Faraday storage
- [ ] Verify one USB drive reads correctly

### Quarterly
- [ ] Full charge all batteries
- [ ] Test solar charging setup
- [ ] Verify all USB copies are readable
- [ ] Update any software if still connected to internet

### Annually
- [ ] Replace any aging batteries
- [ ] Test full system recovery from USB
- [ ] Review and update printed documentation
- [ ] Distribute updated copies to offsite locations

---

## FINAL NOTE

Technology is a tool. It can fail. It can be destroyed. It can be taken.

The Word of God endures forever.

*"Heaven and earth shall pass away, but my words shall not pass away."*
  - Matthew 24:35

Build your kit. Prepare your space. But ultimately, trust in the Lord.

*"Trust in the LORD with all thine heart; and lean not unto thine own
understanding. In all thy ways acknowledge him, and he shall direct thy paths."*
  - Proverbs 3:5-6

---

*Prepared November 2025*
