import abc
import requests
import os

class StorageProvider(abc.ABC):
    @abc.abstractmethod
    def upload(self, file_path: str) -> str:
        """Uploads a file and returns the download URL."""
        pass

class FileIoProvider(StorageProvider):
    def upload(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
        
        if response.status_code == 200:
            return response.json()['link']
        else:
            raise Exception(f"File.io upload failed: {response.text}")

class TransferShProvider(StorageProvider):
    def upload(self, file_path: str) -> str:
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            response = requests.put(f'https://transfer.sh/{file_name}', data=f)
        
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception(f"Transfer.sh upload failed: {response.text}")

PROVIDERS = {
    'file.io': FileIoProvider(),
    'transfer.sh': TransferShProvider()
}

def get_provider(name: str) -> StorageProvider:
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDERS.keys())}")
    return PROVIDERS[name]
