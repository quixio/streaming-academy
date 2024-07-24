import os

from quixstreams.sinks.influxdb_v3 import InfluxDBV3Sink
from quixstreams import Application

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(
    consumer_group="influx-db-sink-v1.5",
    auto_offset_reset="earliest",
    commit_every=1000  # Commit every 1000 offsets
)
topic = app.topic(os.environ["input"])

sink = InfluxDBV3Sink(
    os.environ["INFLUXDB_TOKEN"],
    os.environ["INFLUXDB_HOST"],
    os.environ["INFLUXDB_ORG"],
    os.environ["INFLUXDB_DATABASE"],
    os.environ["INFLUXDB_MEASUREMENT_NAME"])
    

sdf = app.dataframe(topic=topic)

sdf.print()
sdf.sink(sink)

app.run(sdf)