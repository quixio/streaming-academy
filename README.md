# Streaming Academy
This repo contains a code and instructions to support series of episodes of Streaming Academy. This series goal is to teach Data engineers and Software Engineers how to build and develop redistributed fault-tolerant streaming architectures using Kafka and Python. 

## Curriculum
1. Episode 1: Intro to stream processing
   - What is stream processing
   - Motivation
   - Kafka fundamentals
     - Topics
     - Partitions
     - Consumer groups
     - Checkpointing
   - Quix Streams fundamentals
     - Application
     - Produce message
     - DataFrame
     - Output DataFrame
     - Group By (repartition)
     - Reprocessing
2. Episode 2: Stateful data transformations
   - Usecases
   - State fundamentals
   - Basic state operations
   - Windows
   - State recovery
   - Partition reaasigment
   - Changelog topics
3. Episode 3: Realtime ML inteference
   - Architecture introduction
   - Model training
   - Model deployment
   - Model KPIs
   - A/B testing
4. Episode 4: Application development
   - Common ways to integrate stream processing pipelines with end apps
   - WebAPI ingestion
   - WebSocket ingestion
   - WebSocket consumption
   - In-memory views
   - Consumer lag metrics



## Sign up
This step is optional, and you can develop whole pipeline locally but we recommend to use QuixCloud trial for your first project so you don't have to spent time on local infrastructure installation (Kafka or Docker).

Sign up here: https://quix.io/signup

## Create Flask Web Gateway
This service is responsible to receive HTTP Post calls from our Sensor Logger app. 

Go to library, search for source *Flask Web Gateway* and add it to your project. Then deploy service with public access enabled.

After service is deployed, in deployment details you can copy url adress and set it in your sensor logger app. Example url: https://webgateway-tomas-streamingacademy-dev.deployments.quix.io


## Install QuixCloud CLI
Quix CLI helps you to connect to your cloud infrastructure seamlessly as well as helps you with managing your pipeline locally. 

### Installation of Quix CLI

To install the Quix CLI, users have multiple methods depending on their operating system. Here's an expanded installation section including the main ways to install Quix CLI on Linux, macOS, and Windows.

#### For macOS:

- **Install latest version:**

  ```bash
  curl -fsSL https://github.com/quixio/quix-cli/raw/main/install.sh | sudo bash
  ```
  
- **Install with explicit version:**

  ```bash
  curl -fsSL https://github.com/quixio/quix-cli/raw/main/install.sh | sudo bash -s -- -v={version}
  ```

#### For Linux:

- **Install latest version:**

    ```bash
    curl -fsSL https://github.com/quixio/quix-cli/raw/main/install.sh | sudo bash
    ```
    
- **Install with explicit version:**

    ```bash
    curl -fsSL https://github.com/quixio/quix-cli/raw/main/install.sh | sudo bash -s -- -v={version}
    ```

#### For Windows (PowerShell):

- **Install latest version:**

  ```powershell
  iwr https://github.com/quixio/quix-cli/raw/main/install.ps1 -useb | iex
  ```
  
- **Install with explicit version:**

  ```powershell
  $quixCliInstall = (iwr https://github.com/quixio/quix-cli/raw/main/install.ps1 -useb).Content; $version="{version}"; iex "$quixCliInstall"
  ```


## Python VENV
Let's start with creating virtual environment for Python

```
python3 -m venv venv
source venv/bin/activate
```

## Create Data normalization service

```
quix local apps create starter-transformation -p data-normalization
cd data-normalization
pip install -r requirements.txt
```

Open main.py and edit app definition to adjust our app for development:

```python
app = Application.Quix(str(uuid.uuid4()), auto_offset_reset="earliest", use_changelog_topics=False)

input_topic = app.topic(os.environ["input"])
#output_topic = app.topic(os.environ["output"])
```

and comment out output until we have output data in shape:

```
#sdf = sdf.to_topic(output_topic)
```

### Local environment preparation
In order to run your code against Quix Cloud infrastructure, we must sync our local environment with Quix Cloud.

Let's start selecting default project and environment by:

```
quix use
```
Now lets go to app.yaml and change input and output topics as following:

```yaml
name: data-normalization
language: Python
variables:
  - name: input
    inputType: InputTopic
    description: Name of the input topic to listen to.
    defaultValue: raw-data
    required: true
  - name: output
    inputType: OutputTopic
    description: Name of the output topic to write to.
    defaultValue: table-data
    required: true
dockerfile: dockerfile
runEntryPoint: main.py
defaultFile: main.py
```

then we create local `.env` file to inject environment variables into the runtime:
```
quix local vars export
```

This will create `.env` file:
```
Quix__Portal__Api=https://portal-api.platform.quix.io
Quix__Organisation__Id=tomas
Quix__Workspace__Id=tomas-streamingacademy-dev
Quix__Sdk__Token=sdk-749a76aeb6ea48d2b1b2d1abb6a3ca55
input=raw-data
output=table-data
```

These environment variables are then injected into the runtime because of these lines at the top of the `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Data normalization
As you can see in the example message, multiple sensors and multiple timestamps are included in one message from 


