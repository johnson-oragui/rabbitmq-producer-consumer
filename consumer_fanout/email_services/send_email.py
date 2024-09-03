import sys
import signal
import json
import pika
from pika.exceptions import StreamLostError
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import pika.channel

from base.rabbitmq_conn import connect_pika
from config.settings import settings 

EXCHANGE_NAME = 'send_email_fanout_exchange'


def send_email_verification(context: dict):
    """
    Sends an email verification using the provided context.
    
    Args:
        context (dict): A dictionary containing the email and other necessary information.
    
    """
    sender_email = settings.MAIL_USERNAME
    receiver_email = context.get('email')
    password = settings.MAIL_PASSWORD

    # Load the email template directory
    directory = 'consumers_basic/email_services/templates'

    loader=FileSystemLoader(
        searchpath=directory
    )
    env = Environment(
        loader=loader
    )

    # Render the email template with the provided context
    template = env.get_template(
        name='account_verification.html'
    ).render(context)

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Your Verification EMail'
    message['From'] = sender_email
    message['To'] = receiver_email

    message.attach(MIMEText(template, 'html'))

    try:
        # Connect to the mail server and send the email
        with smtplib.SMTP_SSL(settings.MAIL_SERVER, settings.MAIL_PORT) as mail_server:
            mail_server.login(
                user=sender_email,
                password=password
            )
            mail_server.sendmail(
                sender_email,
                receiver_email,
                message.as_string()
            )
    except Exception as exc:
            print(f"Failed to send email: {exc}")

def send_email(ch: pika.channel.Channel,
               method: pika.DeliveryMode,
               properties: pika.BasicProperties,
               body: bytes) -> None:
    """
    Callback function for handling email sending.
    
    Args:
        ch (pika.channel.Channel): The channel object.
        method (pika.DeliveryMode): Delivery method properties.
        properties (pika.BasicProperties): Message properties.
        body (bytes): The message body containing email data.
    
    """
    # Define signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print('Shutting down consumer...')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    data: dict = json.loads(body)
    email = data.get('email')
    first_name = data.get('first_name')

    try:
        # Send email verification using the provided email and first name
        send_email_verification({
            'email': email,
            'first_name': first_name,
            'fake_verification_url': 'https://myapp-app/verify?token=123456'
        })
        print(f'Email sent to {email}')
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f'could not send email: {exc}')
        # Don't acknowledge, so the message can be retried
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    """
    Main function to consume messages from the RabbitMQ exchange and send emails.
    
    Continuously listens for messages on the specified exchange and processes
    them using the send_email callback.
    
    """
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
                    on_message_callback=send_email
                )
                # set the prefetch count to 1 in quality_of_service
                channel.basic_qos(
                        prefetch_count=1
                )

                print('Waiting for to send email...')
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
