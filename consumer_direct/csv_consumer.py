import csv
from uuid import uuid4

def csv_consumer(body: str):
    """Processes CSV data by saving it to a .csv file.
    
    Args:
        body (str): The content to be processed.
    """
    
    print(f"Processing CSV data: {body}")
    message = body.split()
    file_name = f'csv_{str(uuid4())}.csv'
    try:
        with open(file_name, encoding='utf-8', mode='w', newline='') as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(message)
        print(f'csv file saved as {file_name}')
    except Exception as exc:
        print(f'error in exporting csv: {exc}')
        raise Exception from exc
