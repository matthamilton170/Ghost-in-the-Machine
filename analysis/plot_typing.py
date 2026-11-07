import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_PATH = r"C:\dev\ghost-data\Test\events_2026-11-06.csv" 

df = pd.read_csv(DATA_PATH)
df["time"] = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert("America/New_York")

keys = df[df["event_type"] == "key_down"]
per_min = keys.set_index("time").resample("1min").size()

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(per_min.index, per_min.values)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=per_min.index.tz))
ax.set_xlabel("Time of day (Eastern)")
ax.set_ylabel("Key presses per minute")
ax.set_title("Typing activity, 6 Nov 2026")
fig.tight_layout()
fig.savefig("docs/typing_speed.png", dpi=150)
plt.show()