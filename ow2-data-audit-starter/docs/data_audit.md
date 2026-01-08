# OW2 Quickplay Heroes Stats — Data Audit

## Snapshot
- Rows: 288
- Columns: 131
- Heroes: 36
- Skill tiers: 8 (All, Bronze, Silver, Gold, Platinum, Diamond, Master, Grandmaster)
- Roles: Damage, Support, Tank
- Grain: Hero × Skill Tier

## Checks
- Duplicate (Hero, Skill Tier): 0
- Grain violations: 0
- Percent range [0,100]: PASS
- Per-10-min non-negative: PASS
- Role consistent per hero: PASS

## Missingness (top 15)
- Low Health Recalls / 10min: 97.22%
- Healing Accuracy: 97.22%
- Meteor Strike Kills / 10min: 97.22%
- Seismic Slam Kills / 10min: 97.22%
- Rocket Punch Kills / 10min: 97.22%
- Gravitic Flux Kills / 10min: 97.22%
- Accretion Kills / 10min: 97.22%
- Barrage Kills / 10min: 97.22%
- Airtime, %: 97.22%
- Terra Surge Kills / 10min: 97.22%
- Javelin Spin Kills / 10min: 97.22%
- Energy Javelin Kills / 10min: 97.22%
- Amp Matrix Assists / 10min: 97.22%
- Deaths Prevented / 10min: 97.22%
- Death Blossom Kills / 10min: 97.22%
