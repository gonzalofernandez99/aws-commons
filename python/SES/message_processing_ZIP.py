import json
import boto3
import email
from botocore.exceptions import NoCredentialsError
from message_processing import extract_message_id
import zipfile

def get_email_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        s3_response_object = s3.get_object(Bucket=bucket_name, Key=file_key)
        email_content = s3_response_object['Body'].read()
        return email.message_from_bytes(email_content)
    except NoCredentialsError:
        print("No se encontraron credenciales de AWS")
        return None

def read_txt_from_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as myzip:
        for filename in myzip.namelist():
            if filename.endswith('.txt'):
                with myzip.open(filename) as myfile:
                    print(myfile.read().decode())

def extract_zip_attachment(email_message):
    print(email_message)
    for part in email_message.walk():
        if part.get_content_type() == "application/x-zip-compressed":
            data = part.get_payload(decode=True)
            zip_filename = "/tmp/" + part.get_filename()
            with open(zip_filename, 'wb') as f:
                f.write(data)
            print(zip_filename)
            read_txt_from_zip(zip_filename)
                
def lambda_handler(event, context):
    try:
        print(event)
        file_key,subject = extract_message_id(event)
        bucket_name = "name_bucket"
        s3_client = boto3.client('s3')
        print(file_key)
        email_message = get_email_from_s3(bucket_name, file_key)
        if email_message:
            extract_zip_attachment(email_message)
        return {
            'statusCode': 200,
            'body': json.dumps('Prueba - Procesamiento de mensaje exitoso')
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e}')
        }
