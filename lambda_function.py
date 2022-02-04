import logging, boto3, os
import pandas as pd

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
    # New file event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    LOGGER.info(f'New object in bucket: {bucket_name =}, {s3_file_name =}')
    
    # Use boto3 to download the event s3 object key to the /tmp directory.
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket_name, s3_file_name, f'/tmp/{s3_file_name}')
    dl_to_tmp = os.path.isfile('/tmp/' + s3_file_name)
    LOGGER.info(f'File {s3_file_name} downloaded to /tmp/: {dl_to_tmp}')
    
    # Use pandas to read the csv.
    try:
        if s3_file_name[-4:] == '.csv':
            df = pd.read_csv(f'/tmp/{s3_file_name}')
            
            # Log the dataframe head as list of dictionaries
            head_response = df.head().to_dict(orient="records")
            LOGGER.info(f"{head_response}")
            
            # Log dataframe head as is
            LOGGER.info(df.head())
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        LOGGER.info(f'File not found: {s3_file_name}')