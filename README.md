# MapleStory Classic EXP Estimator

A simple browser calculator for estimating expected MapleStory Classic EXP/hour from map data. It does **not** capture the screen, use OBS, or track gameplay.

Open `index.html` directly, or serve the folder locally:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>.

## What to enter

For each monster on the map:

- EXP per monster
- Number of monsters on the map
- Respawn time in seconds

Adjust the assumptions for:

- Party size
- Shots per kill
- Seconds per shot
- Uptime percentage

The result shows expected EXP/hour per character, party EXP/hour, EXP per full map cycle, map cycle time, and full clears/hour.

## Calculation model

The calculator estimates a full-map clear time as:

```text
monster count × shots per kill × seconds per shot ÷ party size
```

The map cycle time is the slower of that clear time and the longest monster respawn time. It then calculates:

```text
party EXP/hour = EXP per map cycle × (3600 ÷ map cycle seconds) × uptime
EXP/hour per character = party EXP/hour ÷ party size
```

This assumes the party distributes work across the map and shares EXP evenly. It is a planning estimate, not a measured in-game rate. Actual rates depend on map layout, movement, spawn behavior, party distribution, misses, looting, downtime, and other gameplay factors.

## Starting map data

The editable defaults are:

- Damp Forest: Slime (12 EXP), Octopus (23 EXP), Jr. Necki (39 EXP)
- The Burnt Land II: Dark Axe Stump (43 EXP), Fire Boar (60 EXP)

Treat monster values, map counts, and respawn times as inputs to verify. The calculator includes a Custom map tab for other maps.
