import requests
from django.conf import settings

def upload_to_pinata(file):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        'pinata_api_key': settings.PINATA_API_KEY,
        'pinata_secret_api_key': settings.PINATA_SECRET_API_KEY,
    }
    files = {'file': file}
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.json().get('IpfsHash')
    else:
        raise Exception("Failed to upload file to Pinata")
