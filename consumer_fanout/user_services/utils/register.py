import signal
import sys
import json
from pika.exceptions import StreamLostError
import time

from base.database import get_db
from consumers_basic.user_services.models import User
from base.rabbitmq_conn import connect_pika
from producers_fanout_method.send_email import send_email_notification

EXCHANGE_NAME = 'register_fanout_exchange'

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
            user_exists = session.query(User).filter_by(email=user_data['email']).first()
            if user_exists:
                print(f' [x] consumer says user with email: {user_exists.email} already exists')
                # Acknowledge message
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            session.add(new_user)
        
        # After successfully adding the user, send an email
        send_email_notification(new_user)

        # Acknowledge the message only if everything was successful
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f"Error processing user registration: {exc}")
        # Don't acknowledge, so the message can be retried
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    def signal_handler(sig, frame):
        print('Shutting down consumer...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while True:
        try:
            with connect_pika() as connection:
                channel = connection.channel()

                # Declare exchange to ensure it exists
                channel.exchange_declare(
                    exchange=EXCHANGE_NAME,
                    exchange_type='fanout',
                    durable=True
                )

                # Declare a unique queue for this consumer
                result = channel.queue_declare(
                    queue='',
                    exclusive=True,
                    durable=True
                )

                queue_name = result.method.queue

                # Bind the queue to the exchange
                channel.queue_bind(
                    queue=queue_name,
                    exchange=EXCHANGE_NAME
                )

                channel.basic_consume(
                    queue=queue_name,
                    exclusive=True,
                    on_message_callback=user_registration
                )

                # set the prefetch count to 1 in quality_of_service
                channel.basic_qos(
                    prefetch_count=1
                )

                print('Waiting for messages...')
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
