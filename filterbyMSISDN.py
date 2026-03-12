import re
import csv
import glob
from datetime import datetime
from collections import defaultdict

# Regex
txn_pattern = r"\[(\d+_\d+)\]"
msisdn_pattern = r"\[(\d{9,15})\]"  # matches MSISDN numbers (9-15 digits)
time_pattern = r"\d{2}-\d{2}@\d{2}:\d{2}:\d{2},\d+"

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

# Transaction dict: {txn_id: {section: [times]}}
transactions = defaultdict(lambda: defaultdict(list))
txn_to_msisdn = {}

def parse_time(t):
    return datetime.strptime(t, "%m-%d@%H:%M:%S,%f")

# Get all log files
log_files = glob.glob("*logs*.txt")
if not log_files:
    print("❌ No log files found in current directory")
    exit()

print(f"📂 Found {len(log_files)} log file(s): {log_files}")

# Parse all log files
for log_file in log_files:
    print(f"🔹 Parsing {log_file}")
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            txn_match = re.search(txn_pattern, line)
            msisdn_match = re.search(msisdn_pattern, line)
            time_match = re.search(time_pattern, line)
            if not txn_match or not msisdn_match or not time_match:
                continue

            txn = txn_match.group(1)
            msisdn = msisdn_match.group(1)
            txn_to_msisdn[txn] = msisdn
            t = parse_time(time_match.group())

            for sec, keywords in sections.items():
                if any(k in line for k in keywords):
                    transactions[txn][sec].append(t)

# Ask user for MSISDN and Transaction ID filters
filter_msisdn = input("Enter MSISDN to filter (leave blank for all): ").strip()
filter_txn = input("Enter Transaction ID to filter (leave blank for all): ").strip()

filtered_txns = {}
for txn, sec_times in transactions.items():
    if filter_msisdn and txn_to_msisdn.get(txn) != filter_msisdn:
        continue
    if filter_txn and txn != filter_txn:
        continue
    filtered_txns[txn] = sec_times

if not filtered_txns:
    print("❌ No transactions found with the given filter(s)")
    exit()

# Compute durations per section
results = []
for txn, secs in filtered_txns.items():
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
        "msisdn": txn_to_msisdn.get(txn, ""),
        "total_time": total_time,
        **section_times
    })

# Sort by total_time
results = sorted(results, key=lambda x: x["total_time"], reverse=True)

# Print summary
print("\n🚀 Transactions Section Times\n")
for r in results:
    print(f"{r['txn']} | MSISDN={r['msisdn']} | Total={r['total_time']:.2f}s | " +
          " | ".join([f"{sec}={t:.2f}s" for sec, t in r.items() if sec not in ['txn','msisdn','total_time']]))

# Export CSV
output_file = "telecom_section_report_filtered.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["TransactionID", "MSISDN", "TotalTime(sec)"] + list(sections.keys()))
    for r in results:
        writer.writerow([r["txn"], r["msisdn"], r["total_time"]] + [r[s] for s in sections.keys()])

print(f"\n📊 Report saved to: {output_file}")
