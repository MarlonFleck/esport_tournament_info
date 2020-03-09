"""
HELPER SCRIPT
When this file is executed it will send the four JSON messages to RabbitMQ
"""
import os
import json
from rabbitConnect import RabbitSender


def load_msg():
    # Load the four given JSON messages. 
    msg = []
    for i in range(4): 
        this_file_name = 'message{}.json'.format(i+1)

        with open(os.path.join('test_json', this_file_name)) as this_json_file:
            msg.append(json.load(this_json_file))

    return msg


if __name__ == '__main__':
    msg = load_msg()
    this_sender = RabbitSender()
    this_sender.send_json(msg)
    print('Four JSON messages were published at RabbitMQ')