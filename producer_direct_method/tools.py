import pika

from base.rabbitmq_conn import connect_pika


EXCHANGE_NAME = 'direct_exchange'

CSV_ROUTING_KEY = 'csv_routing'

DOCS_ROUTING_KEY = 'docs_routing'

SCRIPT_ROUTING_KEY = 'script_routing'

ERROR_ROUTING_KEY = 'error_routing'

WARNING_ROUTING_KEY = 'warning_routing'

def producer(routing_key, message):
    """
    Publishes a message to the direct exchange with a specific routing key.
    
    Args:
        routing_key (str): The routing key to route the message to the correct queue.
        message (str): The message to be sent.
    """
    with connect_pika() as connection:
        channel = connection.channel()

        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='direct',
            durable=True
        )

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode(
                    value=2
                )
            )
        )

        print(f' [x] Sent "{message}" with routing_key "{routing_key}" ')



if __name__ == '__main__':
    producer(CSV_ROUTING_KEY, 'This is a CSV processing task.')
    producer(DOCS_ROUTING_KEY, 'This is a document processing task.')
    producer(SCRIPT_ROUTING_KEY, 'This is a script execution task.')
    producer(ERROR_ROUTING_KEY, 'This is an error log.')
    producer(WARNING_ROUTING_KEY, 'This is a warning log.')
