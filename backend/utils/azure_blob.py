import os
from azure.storage.blob.aio import BlobServiceClient
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

if not AZURE_STORAGE_ACCOUNT or not AZURE_STORAGE_KEY or not AZURE_CONTAINER_NAME:
    raise ValueError("Missing Azure Storage config values")

AZURE_CONNECTION_STRING = (
    f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};"
    f"AccountKey={AZURE_STORAGE_KEY};EndpointSuffix=core.windows.net"
)

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

async def upload_image_to_blob(file):
    file_ext = file.filename.split('.')[-1]
    unique_name = f"{uuid.uuid4().hex}_{datetime.utcnow().timestamp()}.{file_ext}"

    if not AZURE_CONTAINER_NAME or not unique_name:
        raise ValueError("Container name or blob name is missing.")

    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=unique_name)
    await blob_client.upload_blob(await file.read(), overwrite=True)

    return f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{unique_name}"
