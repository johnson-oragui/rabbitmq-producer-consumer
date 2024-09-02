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
