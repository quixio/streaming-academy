import os
from quixstreams import Application, State
from console_sink import ConsoleSink

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()


app = Application(consumer_group="odometer-v1.5", auto_offset_reset="earliest")

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])
console_sink = ConsoleSink()


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

sdf = sdf.hopping_window(10000, 1000, 1000) \
        .reduce(lambda window, row: {**window, **row}, lambda row: row) \
        .final()

sdf = sdf.apply(lambda row: {
    **row["value"],
    "time": row["end"]
})

sdf = sdf.update(console_sink.print_with_metadata, metadata=True)

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)