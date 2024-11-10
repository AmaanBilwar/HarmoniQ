from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os


def create_container(container_name):
    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )

    # Create the container
    container_client = blob_service_client.create_container(container_name)
    return container_client


def upload_blob(container_name, blob_name, file_path):
    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )

    # Create a BlobClient object
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    print(f"Uploading to Azure Storage as blob:\n\t{blob_name}")

    # Upload the created file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    # List the blobs in the container
    print("\nListing blobs...")
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)


if __name__ == "__main__":
    container_name = "testcontainer"  # Ensure the container name is valid
    blob_name = "blobname.txt"  # Ensure the blob name is valid
    file_path = "path/to/your/file.txt"  # Ensure the file path is correct

    create_container(container_name)
    upload_blob(container_name, blob_name, file_path)

    print("Blob uploaded successfully")
