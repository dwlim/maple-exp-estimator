# MapleStory Classic EXP/hour Estimator

A browser calculator for estimating expected MapleStory Classic EXP/hour from map data and the average sustained DPS of each party member. It does not capture the screen or track gameplay.

Live site: <https://dwlim.github.io/maple-exp-estimator/>

## How to use

1. Choose a map.
2. Choose Spearman mode to enter a level, or Details mode to enter average sustained DPS for one party member.
3. Enter party size and uptime percentage.
4. Read the expected EXP/hour for every monster and the total EXP/hour per character.

The starter maps are **Damp Forest** and **The Burnt Land II**. A Custom map tab is included for other maps, but its starter values are placeholders until custom map editing is added.

## Calculation model

The estimator follows OSMS’s weighted EXP model while using party DPS to determine clear speed:

```text
average Spearman DPS = estimated clean-gear Power Strike damage ÷ attack interval in Spearman mode, or manual input in Details mode
combat clear seconds = total map HP ÷ (average DPS per member × party size)
estimated movement seconds = average nearest-spawn travel time ÷ party size
cycle seconds = max(combat clear seconds + estimated movement seconds, OSMS 7.56-second spawn cycle)
full clears/hour = 3600 ÷ cycle seconds × map mob rate × uptime
map EXP/hour = sum(monster EXP × map spawn points) × full clears/hour
EXP/hour per character = map EXP/hour ÷ party size
```

Spearman mode is a transparent approximation for levels 10–70. It assumes clean gear, 25 DEX, 5 STR gained per level after level 10, the OSMS spear progression, Power Strike ramping to 260% by level 30, and a simple 1.5/1.8-second normal/slow attack interval. It averages the estimated Power Strike damage range and does not model misses, monster defense, mastery progression, movement, or multi-target attacks. Details mode accepts manual average DPS. The calculator multiplies member DPS by party size for shared clear speed. OSMS’s 7.56-second cycle is the ceiling: increasing DPS improves the estimate until the party can clear within that cycle. The starter maps add movement time based on the average distance from each OSMS spawn point to its nearest neighboring spawn, then divide that travel time across the party. Damp Forest averages about 107 pixels and The Burnt Land II about 126 pixels before party splitting, using an assumed 180 pixels/second movement speed. This is not an exact player route and does not model ladders, drops, or party positioning. Actual received EXP can still be lower because of missed attacks, kill priority, additional downtime, and uneven party distribution.

## Data source

Monster HP, EXP, and map population defaults are sourced from [OSMS Data Explorer](https://osmsdataexplorer.com/#overview), specifically its public data repository: [ohmi69/osms_datamine_dashboard](https://github.com/ohmi69/osms_datamine_dashboard).

Current starter values:

- Damp Forest: Slime (115 HP, 12 EXP, 2), Octopus (191 HP, 23 EXP, 15), Jr. Necki (272 HP, 39 EXP, 11)
- The Burnt Land II: Dark Axe Stump (547 HP, 43 EXP, 12), Fire Boar (842 HP, 60 EXP, 19)

The calculator uses OSMS’s 7.56-second default spawn cycle and map mob rate. At 100% uptime, Damp Forest approaches about 303,619 map EXP/hour when DPS is high enough; lower DPS produces a proportionally lower rate.

## Local development

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>.
