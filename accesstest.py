import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobBlock, BlobClient, StandardBlobTier


load_dotenv()
keyVaultName = os.getenv('KEY_VAULT_NAME')
KVUri = os.getenv('KEY_VAULT_URI')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
tenant_id = os.getenv('AZURE_TENANT_ID')
account_url = os.getenv('AZURE_ACCOUNT_URL')
container_name=os.getenv('AZURE_CONTAINER_NAME')

credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret,tenant_id=tenant_id)
client = SecretClient(vault_url = KVUri, credential = credential)

#get_secret = client.get_secret(MEDIUM_TOKEN).value

secretName = "appsecret"
secretValue = "my sample app secret cloud"

print(f"Creating a secret in KV_NAME called '{secretName}' with the value '{secretValue}' ...")

client.set_secret(secretName, secretValue)

print(" done.")

print(f"Retrieving your secret from KV_NAME.")

retrieved_secret = client.get_secret(secretName)

print(f"Your secret is '{retrieved_secret.value}'.")

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=credential)
def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str, blob_name: str):
    container_client = blob_service_client.get_container_client(container=container_name)
    with open(file=os.path.join(os.getcwd(), blob_name), mode="rb") as data:
        blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)

upload_blob_file(blob_service_client=blob_service_client, container_name="diversitymatch", blob_name="test-blob.txt")