import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

DATA_PATH = r"C:\dev\ghost-data\events_2026-11-10_162404.csv" 

df = pd.read_csv(DATA_PATH)
df["time"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("America/New_York")

full_index = pd.date_range(df["time"].min().floor("1min"),df["time"].max().floor("1min"), freq="1min")

def per_minute_count(event_type):
    rows = df[df["event_type"] == event_type]
    return rows.set_index("time").resample("1min").size().reindex(full_index, fill_value=0)

keys_per_min = per_minute_count("key_down")
clicks_per_min = per_minute_count("mouse_down")

mv = df[df["event_type"] == "mouse_move"].sort_values("timestamp").copy()
mv["dist"] = np.hypot(mv["x"].diff(), mv["y"].diff())
dist_per_min = (mv.set_index("time")["dist"].resample("1min").sum().reindex(full_index, fill_value=0))



fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 8))
panels = [(keys_per_min, "Key presses / min"),
          (clicks_per_min, "Clicks / min"),
          (dist_per_min, "Mouse distance (px / min)")]

for ax, (series, label) in zip(axes, panels):
    ax.bar(series.index, series.values, width=1/1440)
    ax.set_ylabel(label)

hb = df[df["event_type"] == "heartbeat"]["time"]
gaps = hb.diff()
long = gaps > pd.Timedelta(seconds=90)
for end, gap in zip(hb[long], gaps[long]):
    for ax in axes:
        ax.axvspan(end - gap, end, color="grey", alpha=0.3)

axes[0].set_title("Input activity, 10 Nov 2026")
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=full_index.tz))
axes[-1].set_xlabel("Time of day (Eastern)")
fig.tight_layout()
fig.savefig("docs/activity_overview(10_Nov_2026).png", dpi=150)
plt.show()