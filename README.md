# MapleStory Classic EXP/hour Estimator

A browser calculator for estimating expected MapleStory Classic EXP/hour from map data and your party’s combined sustained DPS. It does not capture the screen or track gameplay.

Live site: <https://dwlim.github.io/maple-exp-estimator/>

## How to use

1. Choose a map.
2. Enter your party’s combined sustained DPS.
3. Enter party size and uptime percentage.
4. Read the expected EXP/hour for every monster and the total EXP/hour per character.

The starter maps are **Damp Forest** and **The Burnt Land II**. A Custom map tab is included for other maps, but its starter values are placeholders until custom map editing is added.

## Calculation model

The party is treated as one shared DPS pool:

```text
map clear seconds = total HP of all monsters on the map ÷ party DPS
cycle seconds = max(map clear seconds, configured respawn lower bound)
full clears/hour = 3600 ÷ cycle seconds × uptime
monster EXP/hour = monster EXP × map count × full clears/hour
EXP/hour per character = total party EXP/hour ÷ party size
```

This is an HP-weighted planning estimate. It assumes the party can distribute its combined DPS across the map and that EXP is shared evenly. Actual results can be lower because of movement, platform travel, spawn placement, missed attacks, kill priority, downtime, and uneven party distribution.

## Data source

Monster HP, EXP, and map population defaults are sourced from [OSMS Data Explorer](https://osmsdataexplorer.com/#overview), specifically its public data repository: [ohmi69/osms_datamine_dashboard](https://github.com/ohmi69/osms_datamine_dashboard).

Current starter values:

- Damp Forest: Slime (115 HP, 12 EXP, 2), Octopus (191 HP, 23 EXP, 15), Jr. Necki (272 HP, 39 EXP, 11)
- The Burnt Land II: Dark Axe Stump (547 HP, 43 EXP, 12), Fire Boar (842 HP, 60 EXP, 19)

The 60-second respawn lower bound is a planning assumption in this version. It should be replaced with verified map respawn data when available.

## Local development

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>.
