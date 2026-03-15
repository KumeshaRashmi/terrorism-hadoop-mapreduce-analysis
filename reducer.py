#!/usr/bin/env python3
import sys

current_type   = None
total_killed   = 0.0
total_wounded  = 0.0
total_incidents = 0

for line in sys.stdin:
    line  = line.strip()
    parts = line.split('\t')
    if len(parts) != 4:
        continue
    attack_type, killed, wounded, count = parts
    try:
        killed  = float(killed)
        wounded = float(wounded)
        count   = int(count)
    except ValueError:
        continue

    if current_type == attack_type:
        total_killed    += killed
        total_wounded   += wounded
        total_incidents += count
    else:
        if current_type:
            avg_k = total_killed  / total_incidents
            avg_w = total_wounded / total_incidents
            print(f"{current_type}\tIncidents:{total_incidents}\t"
                  f"TotalKilled:{total_killed:.0f}\tTotalWounded:{total_wounded:.0f}\t"
                  f"AvgKilled:{avg_k:.2f}\tAvgWounded:{avg_w:.2f}")
        current_type    = attack_type
        total_killed    = killed
        total_wounded   = wounded
        total_incidents = count

# output the last group
if current_type:
    avg_k = total_killed  / total_incidents
    avg_w = total_wounded / total_incidents
    print(f"{current_type}\tIncidents:{total_incidents}\t"
          f"TotalKilled:{total_killed:.0f}\tTotalWounded:{total_wounded:.0f}\t"
          f"AvgKilled:{avg_k:.2f}\tAvgWounded:{avg_w:.2f}")
