import json
import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import pika.channel

from base.rabbitmq_conn import connect_pika
from config.settings import settings 


def send_email_verification(context: dict):
    sender_email = settings.MAIL_USERNAME
    receiver_email = context.get('email')
    password = settings.MAIL_PASSWORD

    directory = 'consumers_basic/email_services/templates'

    loader=FileSystemLoader(
        searchpath=directory
    )
    env = Environment(
        loader=loader
    )

    template = env.get_template(
        name='account_verification.html'
    ).render(context)

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Your Verification EMail'
    message['From'] = sender_email
    message['To'] = receiver_email

    message.attach(MIMEText(template, 'html'))

    try:
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
    data: dict = json.loads(body)
    email = data.get('email')
    first_name = data.get('first_name')

    try:
        # implement send email here
        send_email_verification({
            'email': email,
            'first_name': first_name,
            'fake_verification_url': 'https://myapp-app/verify?token=123456'
        })
        print(f'Email sent to {email}')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f'could not send email: {exc}')
        # Don't acknowledge, so the message can be retried
        ch.basic_nack(delivery_tag=method.delivery_tag)

def main():
    with connect_pika() as connection:
        channel = connection.channel()

        channel.queue_declare(
            queue='send_email'
        )

        channel.basic_consume(
            queue='send_email',
            auto_ack=False,
            on_message_callback=send_email
        )
        print('Waiting for to send email...')
        channel.start_consuming()


if __name__ == '__main__':
    main()
