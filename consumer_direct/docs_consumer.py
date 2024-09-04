from uuid import uuid4

def docs_consumer(body):
    """Processes DOCS data by saving it to a .txt file.
    
    Args:
        body (str): The content to be processed.
    """
    print(f"Processing DOCS data: {body}")
    try:
        # Generate a unique file name for each document
        filename = f'doc_{str(uuid4())}.txt'
        
        # Write the content to a .txt file
        with open(filename, mode='w', encoding='utf-8') as doc_file:
            doc_file.write(body)
        
        print(f'Document saved as {filename}')
    
    except Exception as exc:
        print(f'Error in processing document: {exc}')
        raise Exception from exc
