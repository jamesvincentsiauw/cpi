from logzero import logger
from dotenv import load_dotenv
import pika, time
import os
load_dotenv()

class RabbitPublisher:
    """
    Class to publish asynchronous messages to RabbitMQ server using pika.
    :param username: username to login to RabbitMQ server
    :param password: password for user to login to RabbitMQ server
    :param host: location of RabbitMQ server
    :param port: port to connect to RabbitMQ server on host
    :param vhost: virtual host on RabbitMQ server
    :param queue_name: queue name to publish messages to
    :param number_of_messages: number of messages to publish
    :param message_interval: number of seconds to wait between publishing each message
    """

    def __init__(self):
        logger.info('instantiate amqp connection')
        self._username = os.environ.get('RABBITMQ_USER')
        self._password = os.environ.get('RABBITMQ_PASSWORD')
        self._host = os.environ.get('RABBITMQ_HOST')
        self._port = int(os.environ.get('RABBITMQ_PORT'))
        self._vhost = os.environ.get('RABBITMQ_VHOST')
        self._message_interval = int(os.environ.get('RABBITMQ_MESSAGE_INTERVAL'))
        self._queue_name = os.environ.get('RABBITMQ_QUEUE')
        self._connection = None
        self._channel = None

    def make_connection(self):
        """
        Makes a connection to a RabbitMQ server using the credentials and server info 
        used to instantiate this class.
        """

        credentials = pika.PlainCredentials(self._username, self._password)
        parameters = pika.ConnectionParameters(self._host, self._port, self._vhost, credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        logger.debug("amqp connected successfully...")

    def channel(self):
        """
        Opens channel on RabbitMQ server with current connection.
        """

        self._channel = self._connection.channel()
        logger.debug("amqp channel opened...")

    def declare_queue(self):
        """
        Declares the queue to publish messages to.
        """

        self._channel.queue_declare(queue=self._queue_name, durable=True)
        logger.debug("amqp queue declared....")

    def get_channel(self):
        """
        get channel to publish
        """

        return self._channel

    def publish_message(self, message):
        """
        Publishes messages to queue on RabbitMQ server.
        """

        self._channel.basic_publish(exchange='',
        routing_key=self._queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistant
        ))
        logger.info("published message %s" %(message))
        time.sleep(self._message_interval)
            

    def close_connection(self):
        """
        Close connection to RabbitMQ server.
        """

        self._connection.close()
        logger.debug("amqp connection closed....")

    def run(self):
        """
        Method to run publisher. Makes connection to RabbitMQ server, creates channel,
        sets up queue, publishes required number of messages, and closes the connection.
        """

        self.make_connection()
        self.channel()
        self.declare_queue()
        # self.publish_message()
        # self.close_connection()

class RabbitConsumer:
    """
    Class to consume blocking messages to RabbitMQ server using pika.
    :param username: username to login to RabbitMQ server
    :param password: password for user to login to RabbitMQ server
    :param host: location of RabbitMQ server
    :param port: port to connect to RabbitMQ server on host
    :param vhost: virtual host on RabbitMQ server
    :param queue_name: queue name to consume messages from
    """

    def __init__(self, username, password, host, port, vhost, queue_name):
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._vhost = vhost
        self._queue_name = queue_name
        self._connection = None
        self._channel = None

    def make_connection(self):
        """
        Makes a connection to a RabbitMQ server using the credentials and server info 
        used to instantiate this class.
        """
        credentials = pika.PlainCredentials(self._username, self._password)
        parameters = pika.ConnectionParameters(self._host, self._port, self._vhost, credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        print("Connected Successfully...")

    def channel(self):
        """
        Opens channel on RabbitMQ server with current connection.
        """

        self._channel = self._connection.channel()
        print("Channel opened...")

    def declare_queue(self):
        """
        Declares the queue to publish messages to.
        """

        self._channel.queue_declare(queue=self._queue_name, durable=True)
        print("Queue declared....")
        print(' [*] Waiting for messages. To exit press CTRL+C')

    def on_message(self, channel, method, properties, body):
        """
        Called when a message is received. Sends an acknowledgement that the 
        message has been received.
        :param channel: channel passed through from server on callback
        :param method: message details passed through from server on callback
        :param properties: message properties passed through from server on callback
        :param body: message body passed through from server on callback
        """

        print(" [x] working on %r" % body)
        time.sleep(3)
        print(" [x] Done")
        self._channel.basic_ack(delivery_tag = method.delivery_tag)

    def consume_messages(self):
        """
        Consumes messages that are in the queue on the RabbitMQ server
        """

        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(self._queue_name, self.on_message)
        self._channel.start_consuming()

    def run(self):
        """
        Method to run consumer. Makes connection to RabbitMQ server, creates channel,
        sets up queue, consumes messages.
        """

        self.make_connection()
        self.channel()
        self.declare_queue()
        self.consume_messages()