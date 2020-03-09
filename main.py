"""
MAIN FUNCTION - RUN THIS

When this function is executed it:
 - starts a listener for RabbitMQ messages (that will be saved to the elasticsearch database)
 - starts a flask server that provides the API to get tournament data from the database
"""
from rabbit.rabbitConnect import RabbitReceiver
from elastic import elastic_server
from server import get_server
from settings import logger_name, log_file_name
import logging
import threading
import json

# SETUP THE LOGGER
# Format of the logged files
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=log_file_name, level=logging.INFO, format=fmt)
logger = logging.getLogger(logger_name)
# Add a stream handler so that logs are also printed to console
logger.addHandler(logging.StreamHandler())


def rabbit_listener():
    # This function starts the RabbitMQ listener that will continue to save new messages into the elasticsearch
    # database.
    logger_name_rabbit = logger_name + '.rabbit'
    rabbit_logger = logging.getLogger(logger_name_rabbit)
    # Send three messages in to the channel.
    this_receiver = RabbitReceiver()
    # Read the messages.
    rabbit_logger.info('Starting the listener for RabbitMQ messages on the queue "match_data"')
    this_receiver.receiver_start(rabbit_callback)


def rabbit_callback(ch, method, properties, body):
    # This callback function will be called each time a new RabbitMQ message is received.
    logger_name_rabbit = logger_name + '.rabbit'
    rabbit_logger = logging.getLogger(logger_name_rabbit)
    rabbit_logger.info('Received new RabbitMQ message')
    try:
        # First the byte string JSON has to be parsed as a dict.
        msg_json = body.decode('utf-8')
        msg_dict = json.loads(msg_json)
        # Save the received data to the database.
        elastic_server.post_json(msg_dict)

    except Exception as e:
        rabbit_logger.error(e)


if __name__ == '__main__':
    logger.info('------- START MAIN ---------')
    # Start the listener for messages in RabbitMQ as a thread.
    rabbit_listener_thread = threading.Thread(target=rabbit_listener)
    rabbit_listener_thread.start()
    # Start the flask server that provides the API at "localhost:5000/get_matches".
    app = get_server()
    app.run(debug=False)
