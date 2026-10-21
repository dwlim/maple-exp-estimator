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

The estimator now follows OSMS’s weighted EXP model:

```text
OSMS spawn cycle = 7.56 seconds when no mob-specific cooldown overrides it
spawn cycles/hour = 3600 ÷ OSMS spawn cycle × map mob rate × uptime
map EXP/hour = sum(monster EXP × map spawn points) × spawn cycles/hour
EXP/hour per character = map EXP/hour ÷ party size
```

Party DPS is retained as a planning input/display field, but it no longer limits the OSMS benchmark. OSMS’s map list uses spawn-point counts and adjusts each mob by its average spawn time; its default spawn time is 7.56 seconds. Actual received EXP can still be lower because of movement, platform travel, spawn placement, missed attacks, kill priority, downtime, and uneven party distribution.

## Data source

Monster HP, EXP, and map population defaults are sourced from [OSMS Data Explorer](https://osmsdataexplorer.com/#overview), specifically its public data repository: [ohmi69/osms_datamine_dashboard](https://github.com/ohmi69/osms_datamine_dashboard).

Current starter values:

- Damp Forest: Slime (115 HP, 12 EXP, 2), Octopus (191 HP, 23 EXP, 15), Jr. Necki (272 HP, 39 EXP, 11)
- The Burnt Land II: Dark Axe Stump (547 HP, 43 EXP, 12), Fire Boar (842 HP, 60 EXP, 19)

The calculator uses OSMS’s 7.56-second default spawn cycle and map mob rate. Damp Forest uses mob rate 0.8, producing about 303,619 map EXP/hour before party sharing (matching OSMS’s weighted benchmark).

## Local development

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>.
