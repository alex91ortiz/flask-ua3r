from io import BytesIO
import os
from google.cloud import storage

project_id = 'revol-bb930'
bucket_name = 'staging.revol-bb930.appspot.com'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'revol-bb930-32bc47daf0b5.json'
client = storage.Client(project_id)

def list_files():
    blobs = client.list_blobs(bucket_name)
    return blobs

def get_byte_objfile(blob):
    byte_stream = BytesIO()
    blob.download_to_file(byte_stream)
    byte_stream.seek(0)
    return byte_stream, blob.name