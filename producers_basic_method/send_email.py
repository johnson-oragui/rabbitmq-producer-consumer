import json

from base.rabbitmq_conn import connect_pika
from consumers_basic.user_services.models import User

def send_email_notification(new_user: User):
    with connect_pika() as connection:
        channel = connection.channel()

        channel.queue_declare(
            queue='send_email'
        )

        channel.basic_publish(
            exchange='',
            routing_key='send_email',
            body=json.dumps({
                'email': new_user.email,
                'first_name': new_user.first_name
            })
        )

        print(f" [x] Sent email notification for {new_user.email} ")

