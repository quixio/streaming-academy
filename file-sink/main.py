from quixstreams import Application, message_key
import os
import json

from dotenv import load_dotenv
load_dotenv()

file_writers = {} 

# you decide what happens here!
def sink(message: dict):

    file_name = bytes.decode(message_key())

    writer = file_writers.get(file_name, open(file_name, 'a'))
    
    writer.write(str(json.dumps(message)) + '\n')
    print(f"Stream {file_name} line appended.")

app = Application.Quix("file-sink-v1.1", auto_offset_reset = "latest")

input_topic = app.topic(os.environ["input"])

sdf = app.dataframe(input_topic)

# call the sink function for every message received.
sdf = sdf.update(sink)

if __name__ == "__main__":
    app.run(sdf)