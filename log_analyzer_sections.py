import re
import csv
import glob
from datetime import datetime
from collections import defaultdict

# Auto detect log file
log_files = glob.glob("*logs*.txt")
if not log_files:
    print("❌ No log file found")
    exit()

log_file = log_files[0]
print("📂 Analyzing:", log_file)

# Regex
txn_pattern = r"\[(\d+_\d+)\]"
time_pattern = r"\d{2}-\d{2}@\d{2}:\d{2}:\d{2},\d+"

# Transaction dict
transactions = defaultdict(lambda: defaultdict(list))

def parse_time(t):
    return datetime.strptime(t, "%m-%d@%H:%M:%S,%f")

# Section keywords
sections = {
    "insert_transaction": ["Request inserted in transaction detail", "in exceute transaction action [INSERT]"],
    "check_subscription": ["checkForSubscription", "Procedure Name CheckForSubscription"],
    "hlr_request": ["sending Request to HLR", "successfully got response from HLR"],
    "rateplan_check": ["checkAndFindRatePlan", "Procedure Name CheckAndFindRatePlan"],
    "charging_request": ["sending request to Charging Server", "response from Charging"],
    "set_default_rbt": ["SetDefaultRbt", "setDefaultRbt procedure result"],
    "sms_send": ["sendSms", "sms successfully sent"],
    "txn_end": ["inside endState deleteTxn", "txn detail delete status"]
}

# Parse log file
with open(log_file, "r", encoding="utf-8") as f:
    for line in f:
        txn_match = re.search(txn_pattern, line)
        time_match = re.search(time_pattern, line)
        if not txn_match or not time_match:
            continue
        txn = txn_match.group(1)
        t = parse_time(time_match.group())

        for sec, keywords in sections.items():
            if any(k in line for k in keywords):
                transactions[txn][sec].append(t)

# Compute durations per section
results = []
for txn, secs in transactions.items():
    section_times = {}
    total_time = 0

    for sec, times in secs.items():
        if times:
            start = min(times)
            end = max(times)
            duration = (end - start).total_seconds()
            section_times[sec] = duration
            total_time += duration
        else:
            section_times[sec] = 0

    results.append({
        "txn": txn,
        "total_time": total_time,
        **section_times
    })

# Sort slowest transactions
results = sorted(results, key=lambda x: x["total_time"], reverse=True)

# Print summary
print("\n🚀 Top Slow Transactions with Section Times\n")
for r in results[:10]:
    print(f"{r['txn']} | Total={r['total_time']:.2f}s | " +
          " | ".join([f"{sec}={t:.2f}s" for sec, t in r.items() if sec not in ['txn','total_time']]))

# Export to CSV
output_file = "telecom_section_report.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["TransactionID", "TotalTime(sec)"] + list(sections.keys()))
    for r in results:
        writer.writerow([r["txn"], r["total_time"]] + [r[s] for s in sections.keys()])

print(f"\n📊 Section-level report saved to: {output_file}")
