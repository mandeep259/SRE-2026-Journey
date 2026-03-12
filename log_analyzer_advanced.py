import re
import csv
import glob
from datetime import datetime
from collections import defaultdict

# Auto detect log file
log_files = glob.glob("*logs*.txt")

if not log_files:
    print("No log file found")
    exit()

log_file = log_files[0]
print("Analyzing:", log_file)

# Regex patterns
txn_pattern = r"\[(\d+_\d+)\]"
time_pattern = r"\d{2}-\d{2}@\d{2}:\d{2}:\d{2},\d+"

# Track transactions
transactions = defaultdict(list)

# Latency trackers
hlr_start = {}
charging_start = {}

hlr_latency = {}
charging_latency = {}

def parse_time(t):
    return datetime.strptime(t, "%m-%d@%H:%M:%S,%f")

with open(log_file, "r", encoding="utf-8") as f:
    for line in f:

        txn_match = re.search(txn_pattern, line)
        time_match = re.search(time_pattern, line)

        if not txn_match or not time_match:
            continue

        txn = txn_match.group(1)
        t = parse_time(time_match.group())

        transactions[txn].append(t)

        # HLR request start
        if "sending Request to HLR" in line:
            hlr_start[txn] = t

        if "successfully got response from HLR" in line:
            if txn in hlr_start:
                hlr_latency[txn] = (t - hlr_start[txn]).total_seconds()

        # Charging request start
        if "sending request to Charging Server" in line:
            charging_start[txn] = t

        if "response from Charging" in line:
            if txn in charging_start:
                charging_latency[txn] = (t - charging_start[txn]).total_seconds()


results = []

for txn, times in transactions.items():

    start = min(times)
    end = max(times)

    total = (end - start).total_seconds()

    results.append({
        "txn": txn,
        "start": start,
        "end": end,
        "total_time": total,
        "hlr_latency": hlr_latency.get(txn, 0),
        "charging_latency": charging_latency.get(txn, 0)
    })

# Sort slowest transactions
results = sorted(results, key=lambda x: x["total_time"], reverse=True)

print("\nTop Slow Transactions\n")

for r in results[:10]:
    print(
        f"{r['txn']} | total={r['total_time']:.2f}s | "
        f"HLR={r['hlr_latency']:.2f}s | "
        f"Charging={r['charging_latency']:.2f}s"
    )

# Export report
output = "telecom_performance_report.csv"

with open(output, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "TransactionID",
        "StartTime",
        "EndTime",
        "TotalTime(sec)",
        "HLR_Latency(sec)",
        "Charging_Latency(sec)"
    ])

    for r in results:
        writer.writerow([
            r["txn"],
            r["start"],
            r["end"],
            r["total_time"],
            r["hlr_latency"],
            r["charging_latency"]
        ])

print("\nReport generated:", output)
