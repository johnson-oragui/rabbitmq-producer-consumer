import json
import pika

from base.rabbitmq_conn import connect_pika
from consumers_basic.user_services.models import User

EXCHANGE_NAME = 'send_email_fanout_exchange'

def send_email_notification(user: User):
    with connect_pika() as connection:
        channel = connection.channel()

        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='fanout',
            durable=True
        )

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key='',
            body=json.dumps({
                'email': user.email,
                'first_name': user.first_name,
                'fake_verification_link': ''
            }),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

        print(f' [x] Sent User data for email verification: {user.email} ')


if __name__ == '__main__':
    user_data = User(**{
        'first_name': input("Enter your first name: ").strip(),
        'email': input("Enter your email: ").strip(),
        'last_name': input("Enter your last name: ").strip(),
        'username': input("Enter your username: ").strip()
    })
    try:
        send_email_notification(user_data)
    except KeyboardInterrupt:
        print('Process stopped')
