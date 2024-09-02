import json

from base.database import get_db
from consumers_basic.user_services.models import User
from base.rabbitmq_conn import connect_pika
from producers_basic_method.send_email import send_email_notification

def user_registration(ch, method, properties, body):
    user_data = json.loads(body)

    new_user = User(
        email=user_data['email'],
        username=user_data['username'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )

    try:
        with get_db() as session:
            session.add(new_user)
        
        # After successfully adding the user, send an email
        send_email_notification(new_user)

        # Acknowledge the message only if everything was successful
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f"Error processing user registration: {exc}")
        # Don't acknowledge, so the message can be retried
        ch.basic_nack(delivery_tag=method.delivery_tag)

def main():
    while True:
        with connect_pika() as connection:
            channel = connection.channel()

            channel.queue_declare(
                queue='register'
            )

            channel.basic_consume(
                queue='register',
                auto_ack=False,
                on_message_callback=user_registration
            )
        print('Waiting for messages...')
        channel.start_consuming()


if __name__ == '__main__':
    main()
