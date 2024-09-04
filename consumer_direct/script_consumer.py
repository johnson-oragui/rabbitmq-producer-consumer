import time


def script_consumer(body):
    print(f"Processing scripts data: {body}")
    time.sleep(5)
    print(f'done processing script data')
