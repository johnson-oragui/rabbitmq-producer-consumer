import pika
from contextlib import contextmanager

import pika.exceptions

@contextmanager
def connect_pika():
    connection_params = pika.ConnectionParameters(
        host='localhost',
        heartbeat=60,  # Set the heartbeat interval to 60 seconds
    )
    connection = pika.BlockingConnection(
        connection_params
    )
    try:
        yield connection
    except pika.exceptions.AMQPConnectionError:
        raise
