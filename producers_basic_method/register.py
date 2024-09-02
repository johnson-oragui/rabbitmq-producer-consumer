import json
from base.rabbitmq_conn import connect_pika


def register_user(data: dict):
    with connect_pika() as connection:
        channel = connection.channel()

        channel.queue_declare(
            queue='register',
        )

        channel.basic_publish(
            exchange='',
            routing_key='register',
            body=json.dumps(data)
        )

        print(f' [x] Sent User data: {data} ')
        

if __name__ == '__main__':
    user_data = {
        'first_name': input("Enter your first name: ").strip(),
        'last_name': input("Enter your last name: ").strip(),
        'email': input("Enter your email: ").strip(),
        'username': input("Enter your username: ").strip()
    }
    try:
        register_user(user_data)
    except KeyboardInterrupt:
        print('process stopped')
