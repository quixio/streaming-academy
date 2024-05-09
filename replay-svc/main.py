from quixstreams import Application
import time
import os
import json

# import the dotenv module to load environment variables from a file
from dotenv import load_dotenv

load_dotenv(override=False)

# Create an Application.
app = Application.Quix()

# Define the topic using the "output" environment variable
topic_name = os.getenv("output", "")
if topic_name == "":
    raise ValueError("The 'output' environment variable is required. This is the output topic that data will be published to.")

topic = app.topic(topic_name)


# Create a pre-configured Producer object.
# Producer is already setup to use Quix brokers.
# It will also ensure that the topics exist before producing to them if
# Application.Quix is initiliazed with "auto_create_topics=True".
producer = app.get_producer()

with producer:
    with open("../file-sink/demo_stream.json", 'r') as file:
        for line in file:
            try:
                # Remove newline characters from the message
                message = json.loads(line.strip())
                
                # Publish message to Kafka
                producer.produce(topic.name, json.dumps(message), "demo_stream.json")

                print(message)

                time.sleep(1)
            except Exception as ex:
                print(str(ex))
                print(line.strip())

    producer.flush(30)  # Wait for all messages to be delivered
    print('All messages have been flushed to the Kafka topic')