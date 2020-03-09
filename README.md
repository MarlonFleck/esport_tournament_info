# INTRODUCTION
Hello, 

thank you for the invitation to this coding challenge. In the following I want to explain 
my approach of solving it. 

## TECHNOLOGY STACK
As a technology stack I chose a RabbitMQ server and an elasticsearch database, both as docker containers. 
Both containers are kept very simple with the default ports and both can be started with the 
docker-compose.yml file provided. 

To save new RabbitMQ messages into the elasticsearch database, a Python program is provided. It 
continuously listens for new RabbitMQ messages and saves them to a database. As suggested, 
the Python package pika is used for communicating with the RabbitMQ server. The queue for the 
messages is called "match_data".

For the communication of the Python program with the elasticsearch database, the Python package 
elasticsearch_dsl is used. The data structure provided by the sample JSON files was used to create 
an elasticsearch document template. 

For the API, a flask server was chosen as a lightweight, easy to set up and reliable framework. 
The package flask_restful is used. Via the address localhost:5000/get_matches the API can be used 
to query the elasticsearch database. The filter options are further explained in the section API.
 
In the Python code logging was implemented. The logging information will be saved in "logfile.log".

## NOTE - EXAMPLE JSON FILES
The example JSON files provided had excessive commas and thereby did not comply to the standard JSON 
format. Due to time limitations of this challenge I deleted these commas by hand and saved the updated 
files in the subfolder "test_json".

# SETUP
The following four steps are necessary to get the system up and running. The commands have to be executed
from the top level folder. The shown commands are for Windows, for Linux, backslashes in the paths have 
to be changed to slashes.

## 1. STARTING RABBITMQ AND ELASTICSEARCH
To start RabbitMQ and elasticsearch, run the docker-compose.yml file with the command:

```
docker-compose up
```

## 2. INSTALL REQUIRED PYTHON PACKAGES
The required Python packages can be installed with the following command: 

```
pip3 install -r .\requirements.txt
```

## 3. PUBLISH TEST JSON TO RABBITMQ
Once the RabbitMQ server is up, the four provided JSON test files can be published to RabbitMQ 
by running the Python file "rabbit_publish_test_msg.py" with the following command: 

```
python3 .\rabbit\rabbit_publish_test_msg.py
```

## 4. START RABBITMQ LISTENER AND FLASK API SERVER
By running the main.py file, the following process are started: 
- Starting a RabbitMQ listener, that automatically saves new messages to the elasticsearch database
- Starting an API flask server that provides an API to query the elasticsearch database
  - If the elasticsearch database was not initiated before, this is automatically done here

```
python3 .\main.py
```

Now everything is up and running and the API can be used.

# API
Once the setup steps were made, the API can be reached with a get request at http://localhost:5000/get_matches. 
Without filters the request returns all match data in the database. To filter the results, the following 
parameters for the get request can be set: 

1. date_start_gte: Only show results that started at/after date_start_gte (in the format "yyyy-mm-dd HH:MM:SS")
2. date_start_lte: Only show results that started at/before date_start_lte (in the format "yyyy-mm-dd HH:MM:SS")
3. tournament: Filter by the name of the tournament 
4. title: Filter by title name 
5. state: Filter by state 

The search is not case sensitive. Multiple filters can be combined. 

As an example, a get request that only shows results of tournaments starting at/before 2020-01-07 15:10:00: 

- http://localhost:5000/get_matches?date_start_lte=2020-01-07 15:10:00

# ASSUMPTIONS
While not further specified, the following assumptions for handling the data were made:

1. The JSON messages send to RabbitMQ are in a valid JSON format (in the example messages were format 
errors caused by extra commas).
2. Each message is uniquely identified by the data field "id". If a second message with the same ID is 
send, it overwrites the first message.
3. The field "tournament" is given either as JSON with an ID and a name or as a sting, which will then 
be interpreted as the name.
    - A filter for "tournament" filters for tournament names
4. The field "scores" is given as a list of JSON objects, each with the fields:
    - "team" as integer
    - "score" as integer
    - "winner" as boolean
5. The  field "teams" is given as a list of JSON objects, each with the fields:
    - "id" as integer 
    - "name" as string
6. The field "date_start_text" is always given in the format "yyyy-mm-dd HH:MM:SS"

# NOTES FROM THE AUTHOR

The project is fully functional and the required features are implemented. I am not sure if I exactly 
understood your idea of what information the API should provide. But from here on the code can easily be 
adjusted to change the data format accordingly. 

Further, the code base is in a good state, but there are further optimizations I did not do due to the 
time limitation. A few things that could easily be improved are, for example:
- checking the format/validity of new data and converting it, if needed, before pushing it to the database
- allow more input formats (e.g. for the date format)
- more code automation (e.g. keywords like "tournament" are hardcoded at several places)
- the logger logs info from third party packages which could be prevented

Finally, file structure was chosen to keep the project compact. That is, for example, 
why all the elastic search insertion and query logic is put in one file (elasticConnect.py). For bigger
projects this should be separated further to increase maintainability and to prevent excessive file sizes.
 
If you have questions or remarks, please contact me. I look forward to hearing back from you. 
 
Best regards, 
Marlon




