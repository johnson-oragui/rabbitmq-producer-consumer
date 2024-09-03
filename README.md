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
**Definition**:
A Fanout exchange routes messages to all of the queues that are bound to it, without taking into account any routing keys. This type of exchange is similar to a broadcast mechanism.

**Routing Logic:**
It ignores the routing key. Messages sent to a fanout exchange are delivered to all queues bound to that exchange, regardless of any criteria.

**Use Case**:
Fanout exchanges are typically used when the same message needs to be sent to multiple consumers simultaneously. For example, broadcasting notifications to all connected users, sending log messages to multiple log-processing systems, or sending updates to multiple services.

**Behavior**:
Every queue that is bound to the exchange receives a copy of every message. There is no filtering based on any attributes of the message.

**Example Scenario:**
Imagine a sports news app where you want to notify all subscribers whenever there is breaking news. By using a Fanout exchange, every subscriber queue will get a notification regardless of their interests(be it in tennis, football, or basketball).

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

## DIRECT EXCHANGE (ROUTING)
**Definition**:
A Direct exchange routes messages to queues based on the message's routing key. The routing key is compared to the binding key of the queues, and messages are routed accordingly.

**Routing Logic**:
The message will be delivered to the queue(s) whose binding key exactly matches the routing key of the message.

**Use Case:**
Direct exchanges are used when you want to route messages to specific queues based on some criteria. For instance, directing messages to different services or workers based on task type, handling different severity levels in a logging system, or sending emails of different types (e.g., verification, newsletter, etc.) to different consumers.

**Behavior**:
Only queues that have a binding key that matches the routing key of the message will receive the message. This allows selective message delivery.

**Example Scenario:**
Consider an e-commerce system where different queues handle different types of notifications: one for order confirmations and another for shipping updates. By using a Direct exchange with appropriate routing keys (order_confirmation and shipping_update), you can ensure that each message goes to the correct processing queue.

# Difference between direct and fanout
### Summary of Differences

| Aspect                | Fanout Exchange                          | Direct Exchange (Routing)                    |
|-----------------------|------------------------------------------|----------------------------------------------|
| **Message Routing**   | Sends to all bound queues                | Sends to specific queues based on routing key |
| **Routing Key**       | Ignored                                  | Used to determine which queue receives the message |
| **Binding Key**       | Not used                                 | Must match routing key to receive messages   |
| **Use Case**          | Broadcasting messages                    | Selective message delivery                   |
| **Common Applications** | Notifications, broadcasting events     | Task distribution, different log levels, specific event handling |

## TOPIC EXCHANGE

## HEADERS EXCHANGE
