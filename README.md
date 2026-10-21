# MapleStory Classic EXP/hour Estimator

A browser calculator for estimating expected MapleStory Classic EXP/hour from map data and the average sustained DPS of each party member. It does not capture the screen or track gameplay.

Live site: <https://dwlim.github.io/maple-exp-estimator/>

## How to use

1. Choose a map.
2. Choose Spearman mode to enter a level, or Details mode to enter average sustained DPS for one party member.
3. Enter party size and uptime percentage.
4. Read the expected EXP/hour for every monster and the total EXP/hour per character.
5. Compare Victoria Island maps in the results table, sorted highest to lowest EXP/hour per character; click a row to expand its mob details.

The calculator currently includes the 182 Victoria Island maps with usable monster spawn data. Damp Forest is selected by default.

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

Spearman mode is a transparent approximation for levels 10–70. It assumes clean gear, 25 DEX, 5 STR gained per level after level 10, the OSMS spear progression, Power Strike ramping to 260% by level 30, and a simple 1.5/1.8-second normal/slow attack interval. It averages the estimated Power Strike damage range and does not model misses, monster defense, mastery progression, movement, or multi-target attacks. Details mode accepts manual average DPS. The calculator multiplies member DPS by party size for shared clear speed. OSMS’s 7.56-second cycle is the ceiling: increasing DPS improves the estimate until the party can clear within that cycle. Each Victoria Island map adds movement time based on the average distance from each OSMS spawn point to its nearest neighboring spawn, then divides that travel time across the party. Damp Forest averages about 107 pixels and The Burnt Land II about 126 pixels before party splitting, using an assumed 180 pixels/second movement speed. This is not an exact player route and does not model ladders, drops, or party positioning. Actual received EXP can still be lower because of missed attacks, kill priority, additional downtime, and uneven party distribution.

## Data source

Monster HP, EXP, and map population defaults are sourced from [OSMS Data Explorer](https://osmsdataexplorer.com/#overview), specifically its public data repository: [ohmi69/osms_datamine_dashboard](https://github.com/ohmi69/osms_datamine_dashboard).

The map dropdown and results table use the Victoria Island subset of OSMS `maps.json` and `monsters.json`, combining each map’s mob spawn positions with monster HP and EXP. Maps without usable monster spawn data are excluded.

The calculator uses OSMS’s 7.56-second default spawn cycle and map mob rate. At 100% uptime, Damp Forest approaches about 303,619 map EXP/hour when DPS is high enough; lower DPS produces a proportionally lower rate.

## Local development

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>.
