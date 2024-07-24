import os
from quixstreams import Application
from console_sink import ConsoleSink
from datetime import timedelta, datetime

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="downsampling-v1.2", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])
console_sink = ConsoleSink(metadata=True, max_columns=10, table_width=100)


sdf = app.dataframe(input_topic)

# Lets calculate feature g-total to represent all 3 axes.
sdf = sdf[sdf.contains("accelerometer-x")]
sdf["g-total"] = sdf["accelerometer-x"].abs() + sdf["accelerometer-y"].abs() + sdf["accelerometer-z"].abs() 

# Reduce window state and new incoming row. 
def window_reduce(window: dict, row:dict):
    window["g-sum"] += row["g-total"]
    window["g-max"] = max(window["g-max"], row["g-total"])
    window["g-count"] += 1

    # For GPS we just remember last position coordinates.
    window["lat"] = row["location-latitude"]
    window["lon"] = row["location-longitude"]

    return window

def window_init(row: dict):
    return {
        "g-sum": row["g-total"],
        "g-max": row["g-total"],
        "g-count": 1,
        "lat": row["location-latitude"],
        "lon": row["location-longitude"]
    }

sdf = sdf.tumbling_window(timedelta(seconds=10), timedelta(seconds=1)) \
    .reduce(window_reduce, window_init) \
    .final()

sdf = sdf.apply(lambda row: {
    "g-mean": row["value"]["g-sum"] / row["value"]["g-count"],
    "g-max": row["value"]["g-max"],
    "lat": row["value"]["lat"],
    "lon": row["value"]["lon"]
})

sdf = sdf.sink(console_sink)

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)