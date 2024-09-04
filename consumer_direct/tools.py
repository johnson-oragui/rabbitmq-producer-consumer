import sys
import signal
from pika.exceptions import StreamLostError
import time

from base.rabbitmq_conn import connect_pika
from consumer_direct.csv_consumer import csv_consumer
from consumer_direct.docs_consumer import docs_consumer
from consumer_direct.error_consumer import error_consumer
from consumer_direct.warning_consumer import warning_consumer
from consumer_direct.script_consumer import script_consumer

EXCHANGE_NAME = 'direct_exchange'

CSV_ROUTING_KEY = 'csv_routing'
DOCS_ROUTING_KEY = 'docs_routing'
SCRIPT_ROUTING_KEY = 'script_routing'
ERROR_ROUTING_KEY = 'error_routing'
WARNING_ROUTING_KEY = 'warning_routing'


def process_message(ch, method, properties, body: bytes):
    """Process messages based on the routing key.

    Args:
        ch: The channel object.
        method: Method object with delivery info and properties.
        properties: Properties object with message metadata.
        body: The message body in bytes.
    """
    routing_key = method.routing_key

    message = body.decode(
        encoding='utf-8'
    )
    try:
        if routing_key == CSV_ROUTING_KEY:
            csv_consumer(message)
        elif routing_key == DOCS_ROUTING_KEY:
            docs_consumer(message)
        elif routing_key == SCRIPT_ROUTING_KEY:
            script_consumer(message)
        elif routing_key == ERROR_ROUTING_KEY:
            error_consumer(message)
        elif routing_key == WARNING_ROUTING_KEY:
            warning_consumer(message)
        else:
            print(f"Unknown routing key: {routing_key}")

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as exc:
        print(f'Error processing message: {exc}')
        # Nack the message and requeue it for another try
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """main

    Return: None
    """
    
    def signal_handler(sig, frame):
        print('shutting down')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        try:
            with connect_pika() as connection:
                channel = connection.channel()

                # Declare the exchange
                channel.exchange_declare(
                    exchange=EXCHANGE_NAME,
                    exchange_type='direct',
                    durable=True
                )

                # Declare a queue and bind it to the routing keys
                result = channel.queue_declare(
                    queue='',
                    exclusive=True,
                    durable=True
                )

                # get the queue name
                queue_name = result.method.queue

                # Bind the queue to specific routing keys
                channel.queue_bind(
                    queue=queue_name,
                    exchange=EXCHANGE_NAME,
                    routing_key=CSV_ROUTING_KEY
                )
                channel.queue_bind(
                    queue=queue_name,
                    exchange=EXCHANGE_NAME,
                    routing_key=DOCS_ROUTING_KEY
                )
                channel.queue_bind(
                    queue=queue_name,
                    exchange=EXCHANGE_NAME,
                    routing_key=WARNING_ROUTING_KEY
                )
                channel.queue_bind(
                    queue=queue_name,
                    exchange=EXCHANGE_NAME,
                    routing_key=ERROR_ROUTING_KEY
                )
                channel.queue_bind(
                    queue=queue_name,
                    exchange=EXCHANGE_NAME,
                    routing_key=SCRIPT_ROUTING_KEY
                )
                # The queue is bound to each specific routing key.
                # This allows the consumer to receive messages that match any of these routing keys.

                # Start consuming messages
                channel.basic_consume(
                    queue=queue_name,
                    on_message_callback=process_message
                )

                # Ensure only one message is processed at a time
                channel.basic_qos(
                    prefetch_count=1
                )

                print("Waiting for messages...")
                channel.start_consuming()
        except StreamLostError as exc:
            print(f"Stream connection lost: {exc}. Reconnecting...")
            # Wait before reconnecting to avoid rapid retries
            time.sleep(5)
        except Exception as exc:
            print(f"An unexpected error occurred: {exc}. Reconnecting...")
            # Handle other exceptions and retry
            time.sleep(5)
            


if __name__ == '__main__':
    main()
