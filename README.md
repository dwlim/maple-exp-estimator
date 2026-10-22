# MapleStory Classic EXP/hour Estimator

A browser calculator for estimating expected MapleStory Classic EXP/hour from map data and the average sustained DPS of each party member. It does not capture the screen or track gameplay.

Live site: <https://dwlim.github.io/maple-exp-estimator/>

## How to use

1. Choose a map.
2. Choose Warrior mode to enter a level, or Details mode to enter average sustained DPS for one party member.
3. Enter party size, uptime percentage, and OSMS monster attack data is used for potion costs.
4. Read the expected EXP/hour for every monster and the total EXP/hour per character.
5. Compare Victoria Island maps in the results table, sorted highest to lowest EXP/hour per character for the selected party size; the table also shows fixed 4-player and 6-player rates. Click a row to expand its mob details.

The calculator includes Victoria Island maps with usable monster spawn data and excludes maps whose bundled monsters provide zero total EXP, such as placeholder/event areas. Damp Forest is selected by default.

## Calculation model

The estimator follows OSMS’s weighted EXP model while using party DPS, map capacity, and single-target attack timing to determine clear speed:

```text
average Warrior DPS = estimated clean-gear Power Strike damage ÷ attack interval in Warrior mode, or manual input in Details mode
damage per attack = average DPS per member × 1.8 seconds, using attack speed 7
active mob count = map capacity, or the raw spawn count when no capacity override is available
active mob factor = active mob count ÷ raw spawn count; this scales active combat workload, not OSMS weighted EXP production
attacks required = sum(ceil(monster HP ÷ damage per attack) × map count × active mob factor)
combat clear seconds = attacks required × 1.8 seconds ÷ party size
estimated movement seconds = slowest parallel area estimate, where spawn points are split into party-sized bands along the map’s dominant dimension and each area uses local nearest-spawn travel plus 10% of its diagonal and a total-mob-count adjustment
effective clear seconds = max(combat clear seconds, estimated movement seconds), because movement and attacking can overlap
cycle seconds = max(effective clear seconds, OSMS 7.56-second spawn cycle)
full clears/hour = 3600 ÷ cycle seconds × map mob rate × uptime
map EXP/hour = sum(monster EXP × map spawn points) × full clears/hour; OSMS weighted EXP already represents the map’s spawn production, so active-capacity scaling is not applied again to EXP
EXP/hour per character = map EXP/hour ÷ party size
estimated player WDEF = round(4 + (level − 10) × 2.5), representing clean Warrior armor from about 4 WDEF at level 10 to 154 at level 70
HP potion cost/hour per character = sum(max(1, OSMS PADamage − estimated player WDEF) × mob count) × full clears/hour ÷ party size ÷ 2, using 1 meso = 2 HP
```

Warrior, Cleric, Fire/Poison, Ice/Lightning, Assassin, Bowman, and Bandit modes are transparent approximations for levels 10–70. Assassin uses Lucky 7, Bowman uses Arrow Blow, and Bandit uses Savage Blow; Assassin, Bowman, and Bandit use 72% of equivalent Warrior WDEF. Assassin movement loss is 50% of melee, Bowman movement loss is 75% of melee, and Bandit movement loss is 100% of melee. Warrior mode is a transparent approximation for levels 10–70. It assumes a shared clean-gear primary-stat progression for every class: 35 main stat at level 10, +4 per level through level 30, then +5 per level; estimated equipment adds 0 main stat at level 10, rising to 42 by level 70. The selected class uses that progression for STR (Warrior), INT (Cleric), DEX (Bowman), or LUK (Assassin/Bandit), while secondary stats remain simple approximations. Cleric uses Holy Arrow at attack speed 6, 50% of melee movement loss, and receives a 50% damage bonus against the bundled undead/holy-weak monster list. Fire/Poison uses Fire Arrow and Ice/Lightning uses Cold Beam at attack speed 6, each with 50% of melee movement loss and a 50% damage bonus against their bundled elemental-weak monster lists. Warrior uses the OSMS spear progression, Power Strike ramping to 260% by level 30, and a simple 1.5/1.8-second normal/slow attack interval. It averages the estimated Power Strike damage range and does not model misses, monster defense, mastery progression, movement, or multi-target attacks. Details mode accepts manual average DPS. For clear time, the calculator assumes single-target attacks at attack speed 7 (1.8 seconds per attack). It converts average member DPS into damage per attack, rounds each mob up to a whole number of attacks, sums those attacks across the map, and divides the attack time by party size to model parallel party members. This makes both mob count and individual mob HP affect clear time. OSMS’s 7.56-second cycle is the ceiling: increasing DPS improves the estimate until the party can clear within that cycle. Each Victoria Island map estimates movement using parallel area coverage: spawn points are split into party-sized bands along the map’s dominant dimension, each band uses local nearest-spawn travel plus a modest 10%-of-diagonal area penalty, and the slowest band determines movement time. Movement overlaps with combat, so it constrains throughput only when slower than the party’s combat clear time; it is not added as a full extra delay to every clear. This gives broad, evenly splittable maps such as Damp Forest a realistic party-size benefit without imposing an overly long sequential route. It remains an approximation and does not model exact routes, platforms, ladders, or player positioning. Damp Forest averages about 107 pixels and The Burnt Land II about 126 pixels before party splitting, using an assumed 180 pixels/second movement speed. This is not an exact player route and does not model ladders, drops, or party positioning. Actual received EXP can still be lower because of missed attacks, kill priority, additional downtime, and uneven party distribution. Potion costs use OSMS PADamage reduced by estimated player WDEF once per mob kill. The WDEF estimate is a clean Warrior armor approximation that scales from 4 at level 10 to 154 at level 70; Details mode uses the entered DPS but still uses the selected character level for WDEF. Damage is floored at 1 HP per hit. Actual damage can differ because the exact server damage formula, armor, attack frequency, misses, magic attacks, equipment quality, and monster attack behavior are not modeled.

## Data source

Monster HP, EXP, and map population defaults are sourced from [OSMS Data Explorer](https://osmsdataexplorer.com/#overview), specifically its public data repository: [ohmi69/osms_datamine_dashboard](https://github.com/ohmi69/osms_datamine_dashboard).

The map dropdown and results table use the Victoria Island subset of OSMS `maps.json` and `monsters.json`, combining each map’s mob spawn positions with monster HP and EXP. Maps without usable monster spawn data are excluded.

The calculator uses OSMS’s 7.56-second default spawn cycle and map mob rate. At 100% uptime, Damp Forest approaches about 303,619 map EXP/hour when DPS is high enough; lower DPS produces a proportionally lower rate.

## Local development

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>.
