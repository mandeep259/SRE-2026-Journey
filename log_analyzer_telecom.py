import re
import csv
import glob
from datetime import datetime
from collections import defaultdict

# Auto-detect log file
log_files = glob.glob("*logs*.txt")

if not log_files:
    print("❌ No log files found in this directory")
    exit()

log_file = log_files[0]
print(f"📂 Analyzing log file: {log_file}")

# Patterns
txn_pattern = r"\[(\d+_\d+)\]"
time_pattern = r"\d{2}-\d{2}@\d{2}:\d{2}:\d{2},\d+"

transactions = defaultdict(list)

def parse_time(t):
    return datetime.strptime(t, "%m-%d@%H:%M:%S,%f")

# Read log file
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        txn_match = re.search(txn_pattern, line)
        time_match = re.search(time_pattern, line)

        if txn_match and time_match:
            txn = txn_match.group(1)
            time_str = time_match.group()

            try:
                time_obj = parse_time(time_str)
                transactions[txn].append(time_obj)
            except:
                pass

results = []

# Calculate durations
for txn, times in transactions.items():
    start = min(times)
    end = max(times)
    duration = (end - start).total_seconds()

    results.append({
        "txn": txn,
        "start": start,
        "end": end,
        "duration": duration
    })

# Sort by slowest
results = sorted(results, key=lambda x: x["duration"], reverse=True)

print("\n🚀 Top Slow Transactions\n")

for r in results[:10]:
    print(f"{r['txn']} → {r['duration']:.2f} sec")

# Export to CSV
output_file = "transaction_report.csv"

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["Transaction ID", "Start Time", "End Time", "Duration (sec)"])

    for r in results:
        writer.writerow([r["txn"], r["start"], r["end"], r["duration"]])

print(f"\n📊 Report saved to: {output_file}")
