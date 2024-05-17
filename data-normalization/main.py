import os
from quixstreams import Application
import uuid
import json

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application(consumer_group="data-normalisation-v1", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)

sdf = sdf.apply(lambda message: message["payload"], expand=True)

def transpose(row: dict):

    new_row = {
        "time": row["time"]
    }

    for key in row["values"]:
        new_row[row["name"] + "-" + key] = row["values"][key]

    return new_row


sdf = sdf.apply(transpose)

sdf = sdf[sdf.contains("accelerometer-x")]
sdf = sdf[["time", "accelerometer-x", 'accelerometer-y', "accelerometer-z"]]

sdf["accelerometer-total"] = sdf["accelerometer-x"].abs() + sdf["accelerometer-y"].abs() + sdf["accelerometer-z"].abs()

sdf = sdf[sdf["accelerometer-total"] > 50]
sdf = sdf.update(lambda row: print(list(row.values())))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)