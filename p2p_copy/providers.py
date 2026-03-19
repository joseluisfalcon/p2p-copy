import abc
import requests
import os

class StorageProvider(abc.ABC):
    @abc.abstractmethod
    def upload(self, file_path: str, progress_callback=None) -> str:
        """Uploads a file and returns the download URL."""
        pass

class FileIoProvider(StorageProvider):
    def upload(self, file_path: str, progress_callback=None) -> str:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            # Simple wrapper to report progress
            class ProgressFile:
                def __init__(self, file_obj, total, callback):
                    self.file_obj = file_obj
                    self.total = total
                    self.callback = callback
                    self.read_so_far = 0
                def read(self, size=-1):
                    data = self.file_obj.read(size)
                    self.read_so_far += len(data)
                    if self.callback:
                        self.callback(self.read_so_far, self.total)
                    return data
                def __len__(self):
                    return self.total

            headers = {'User-Agent': 'p2p-copy/1.0'}
            response = requests.post(
                'https://www.file.io', 
                files={'file': ProgressFile(f, file_size, progress_callback)}, 
                headers=headers
            )
        
        if response.status_code == 200:
            return response.json()['link']
        else:
            raise Exception(f"File.io upload failed: {response.text}")

class PixelDrainProvider(StorageProvider):
    def upload(self, file_path: str, progress_callback=None) -> str:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            class ProgressFile:
                def __init__(self, f, total, cb):
                    self.f = f
                    self.total = total
                    self.cb = cb
                    self.read_so_far = 0
                def read(self, size=-1):
                    data = self.f.read(size)
                    self.read_so_far += len(data)
                    if self.cb: self.cb(self.read_so_far, self.total)
                    return data
                def __len__(self): return self.total

            response = requests.post('https://pixeldrain.com/api/file', files={'file': ProgressFile(f, file_size, progress_callback)})
        
        if response.status_code == 201 or response.status_code == 200:
            file_id = response.json()['id']
            return f"https://pixeldrain.com/u/{file_id}"
        else:
            raise Exception(f"PixelDrain upload failed (Status {response.status_code}): {response.text}")

class LitterboxProvider(StorageProvider):
    def upload(self, file_path: str, progress_callback=None) -> str:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            class ProgressFile:
                def __init__(self, f, total, cb):
                    self.f = f
                    self.total = total
                    self.cb = cb
                    self.read_so_far = 0
                def read(self, size=-1):
                    data = self.f.read(size)
                    self.read_so_far += len(data)
                    if self.cb: self.cb(self.read_so_far, self.total)
                    return data
                def __len__(self): return self.total

            data = {'reqtype': 'fileupload', 'time': '1h'}
            files = {'fileToUpload': ProgressFile(f, file_size, progress_callback)}
            response = requests.post('https://litterbox.catbox.moe/resources/internals/api.php', data=data, files=files)
        
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception(f"Litterbox upload failed (Status {response.status_code}): {response.text}")

class CustomRelayProvider(StorageProvider):
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def upload(self, file_path: str, progress_callback=None) -> str:
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            # Simple wrapper to report progress
            class ProgressFile:
                def __init__(self, f, total, cb):
                    self.f = f
                    self.total = total
                    self.cb = cb
                    self.read_so_far = 0
                def read(self, size=-1):
                    data = self.f.read(size)
                    self.read_so_far += len(data)
                    if self.cb: self.cb(self.read_so_far, self.total)
                    return data
                def __len__(self): return self.total

            # Simple PUT or POST based on the user's relay
            response = requests.post(self.endpoint_url, files={'file': ProgressFile(f, file_size, progress_callback)})
        
        if response.status_code in [200, 201]:
            # Expecting the relay to return the download URL in the body
            return response.text.strip()
        else:
            raise Exception(f"Custom relay upload failed (Status {response.status_code}): {response.text}")

PROVIDERS = {
    'file.io': FileIoProvider(),
    'pixeldrain': PixelDrainProvider(),
    'litterbox': LitterboxProvider()
}

def get_provider(name: str) -> StorageProvider:
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDERS.keys())}")
    return PROVIDERS[name]
