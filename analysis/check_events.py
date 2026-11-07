import argparse
import glob, os
import sys
import pandas as pd
parser = argparse.ArgumentParser()

KEY_TYPES = {"key_down", "key_up"}
MOUSE_TYPES = {"mouse_move", "mouse_down", "mouse_up"}
HEARTBEAT_INTERVAL = 60
LONG_GAP_S = 300       

parser.add_argument("path", nargs="?")
args = parser.parse_args()
path = args.path or max(glob.glob(r"C:\dev\ghost-data\events_*.csv"), key=os.path.getmtime)
summary_list = []
warnings = []

with open(path, newline="") as f:
    raw_lines = sum(1 for _ in f)
df = pd.read_csv(path, on_bad_lines="skip", dtype=str)
rows_loaded = len(df)
dropped = (raw_lines - 1) - len(df)
df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])
df = df[df["timestamp"] > 1.5e9]

bad_rows = rows_loaded - len(df)
if dropped > 0 or bad_rows > 0:
    warnings.append(f"{dropped} malformed lines skipped, {bad_rows} rows removed for unusable timestamps")

out_of_order = (df["timestamp"].diff() < 0).sum()
if out_of_order > 0:
    warnings.append(f"{out_of_order} rows out of timestamp order")

counts = df["event_type"].value_counts()
duration_s = df["timestamp"].max() - df["timestamp"].min()

print("Counts per type:")
print(counts.to_string())
first_time = pd.to_datetime(df["timestamp"].min(), unit="s", utc=True).tz_convert("America/New_York")
last_time = pd.to_datetime(df["timestamp"].max(), unit="s", utc=True).tz_convert("America/New_York")
print(f"First timestamp: {first_time:%Y-%m-%d %H:%M:%S}")
print(f"Last timestamp: {last_time:%Y-%m-%d %H:%M:%S}")
print(f"Duration: {duration_s / 3600:.2f} hours")

hb = df[df["event_type"] == "heartbeat"]["timestamp"]
print(f"Heartbeats: {len(hb)} (about {duration_s / HEARTBEAT_INTERVAL:.0f} expected)")

if len(hb) == 0:
    warnings.append("no heartbeats (older file, or writer fault)")
else:
    long_hb_gaps = (hb.diff().dropna() > 1.5 * HEARTBEAT_INTERVAL).sum()
    if long_hb_gaps:
        warnings.append(f"{long_hb_gaps} heartbeat gaps over 90 s: logger not running then")

activity = df[df["event_type"] != "heartbeat"].copy()
activity["gap"] = activity["timestamp"].diff()
big = activity[activity["gap"] > LONG_GAP_S].sort_values("gap", ascending=False).head(5)

print("Largest input gaps:")
for _, row in big.iterrows():
    t = pd.to_datetime(row["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    print(f"  {row['gap'] / 60:6.1f} min ending {t:%H:%M:%S}")

types = set(counts.index)
if not types & KEY_TYPES:
    warnings.append("no keyboard events at all")
if not types & MOUSE_TYPES:
    warnings.append("no mouse events at all")

for e in ["mouse_down", "mouse_up"]:
    near_dupes = (df[df["event_type"] == e]["timestamp"].diff() < 0.003).sum()
    if near_dupes:
        warnings.append(f"{near_dupes} near-duplicate {e} events (<3 ms): two loggers running?")

mouse_rows = df[df["event_type"].isin(MOUSE_TYPES)]
if mouse_rows["x"].isna().any():
    warnings.append("some mouse rows have no coordinates")

diff = counts.get("key_down", 0) - counts.get("key_up", 0)
print(f"key_down - key_up = {diff}")

print()
if warnings:
    print("WARNINGS")
    for w in warnings:
        print(" -", w)
    sys.exit(1)
else:
    print("OK: no problems found")