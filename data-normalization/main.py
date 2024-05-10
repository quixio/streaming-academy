import os
from quixstreams import Application

import uuid
import json

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

app = Application.Quix(
    "data-normalization-v1.2",
    auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)


sdf = sdf.apply(lambda row: row["payload"], expand=True)

def transpose(row: dict):

    result = {
        "time": row["time"]
    }

    column_name_prefix = row["name"]

    for dimension in row["values"]:
        result[column_name_prefix + "-" + dimension] = row["values"][dimension]

    return result

sdf = sdf.apply(transpose)        

sdf = sdf.update(lambda row: print(json.dumps(row, indent=4)))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)