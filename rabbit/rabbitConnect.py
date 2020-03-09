"""
A CLASS HANDLING GET/PUT REQUESTS TO RABBITMQ
"""
import pika
import json


class RabbitConnect:
    queue_name = 'match_data'
    connection = None
    channel = None

    def connect(self):
        # Open a connection and channel.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def close(self):
        # Close the connection.
        self.connection.close()


class RabbitSender(RabbitConnect):
    # Send messages to the RabbitMQ queue.
    def send_msg(self, msg): 
        self.connect()
        # Send the message (or multiple messages, if msg is a list of messages).
        if type(msg) == list:
            for this_msg in msg: 
                # Send a message.
                self.channel.basic_publish(exchange='',
                                           routing_key=self.queue_name,
                                           body=this_msg)

        else: 
            # Send a message.
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue_name,
                                       body=msg)

        print("Message was send")
        self.close()
    
    def send_json(self, json_msg):
        self.connect()
        # Send json data (or multiple json data, if json_msg is a list of messages).
        if type(json_msg) == list:
            for this_json in json_msg: 
                # Send a message.
                self.channel.basic_publish(exchange='',
                                           routing_key=self.queue_name,
                                           body=json.dumps(this_json))

        else: 
            # Send a message.
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue_name,
                                       body=json.dumps(json_msg))

        self.close()


class RabbitReceiver(RabbitConnect):
    def callback_receive(self, ch, method, properties, body):
        # Callback function that is executed each time a message is received. 
        print("Data received: {}".format(body))

    def receiver_start(self, callback=None):
        if callback is None:
            callback = self.callback_receive
            
        self.connect()
        # Start receiving messages.
        self.channel.basic_consume(queue=self.queue_name,
                                   auto_ack=True,
                                   on_message_callback=callback)
        # Start consuming the messages in an infinite loop.
        self.channel.start_consuming()

