## rabbitmq-producer-consumer
Contains Rabbitmq information

### Description
Let's build a simple microservice example using Python and RabbitMQ without involving any web development frameworks. We'll use two Python scripts to simulate the microservices: one for handling user registrations (the User Service) and another for sending email notifications (the Email Service).

## Microservices Overview

**User Service:**
Handles user registration and sends a message to RabbitMQ.

**Email Service:**
Listens to RabbitMQ for new user registration messages and sends a welcome email.

## Prerequisites
 - RabbitMQ installed and running locally (or accessible from your network). You can use Docker to run RabbitMQ:
```
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

 - requirements
```
python -m pip install -r requirements.txt --upgrade
```
**list enqueued messages**
```
sudo rabbitmqctl list_queues
```
## To run the project

 * run alembic migration
```
alembic revision -m "initial migrations" --autogenerate
```
```
alembic upgrade head
```

 * start the consumers on different tabs
```
python -m consumers_basic.user_services.utils.register_basic
```

```
python -m consumers_basic.email_services.send_email
```

 * and then run the register producer
```
python -m producers_basic_method.register
```
 * This should prompt you to enter user details

After entering your details, it should be added to the database and email sent to you. There is no need to start the "producers_basic_method.send_email" since it would be called by the register consumer after the user is successfully added to the database.
This is broadcasting messages through routing_key.

## FANOUT EXCHANGE
The fanout exchange does not use queues directly(does not send messages to queues directly or uses a default exchange), an exchange name has to be provided when channel.queue_declare is used.
 * start the consumers on different tabs
```
python -m consumers_fanout.user_services.utils.register
```

```
python -m consumers_fanout_method.email_services.send_email
```

 * and then run the register producer of the fanout method
```
python -m producers_fanout_method.register
```
This time, faker module is used to generate fake user details, you can always switch them for real emails, since the send_email consumer would send emails to the users' emails.
## TOPIC EXCHANGE

## DIRECT EXCHANGE

## HEADERS EXCHANGE
