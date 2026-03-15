#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
header = next(reader, None)  # skip the header row

for row in reader:
    try:
        attack_type = row[29].strip()   # attacktype1_txt column
        nkill  = float(row[98])  if row[98].strip()  not in ['', '.'] else 0.0
        nwound = float(row[102]) if row[102].strip() not in ['', '.'] else 0.0
        if attack_type:
            print(f"{attack_type}\t{nkill}\t{nwound}\t1")
    except (IndexError, ValueError):
        pass
