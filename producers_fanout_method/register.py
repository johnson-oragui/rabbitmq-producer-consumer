import json
from faker import Faker
import pika

from base.rabbitmq_conn import connect_pika

EXCHANGE_NAME = 'register_fanout_exchange'

def register_user(data: dict):
    with connect_pika() as connection:
        channel = connection.channel()

        # Declare a fanout exchange
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='fanout',
            durable=True
        )

        # Publish to the exchange, not directly to a queue
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key='',
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        print(f' [x] Sent User data: {data} ')


if __name__ == '__main__':
    faker = Faker()
    for i in range(50):
        user_data = {
            'email': faker.email(),
            'first_name': faker.unique.first_name(),
            'last_name': faker.name(),
            'username': faker.name()
        }
        try:
            register_user(user_data)
        except KeyboardInterrupt:
            print('Process stopped')
