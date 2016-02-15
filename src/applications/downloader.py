import hashlib
import shutil

import os
import requests


class Downloader:
    def __init__(self):
        pass

    def download(self, application, destination):
        if os.path.isfile(destination):
            print('already downloaded ' + application.filename())
            return

        print(application.url())
        response = requests.get(application.url(), stream=True)
        print(response.status_code)
        with open(destination, "wb") as storage_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    storage_file.write(chunk)
                    storage_file.flush()


class ArchivingDownloader:
    def __init__(self, archive_directory, downloader):
        self.archive_directory = archive_directory
        self.downloader = downloader

    def download(self, application, destination):
        archive_key = hashlib.md5(destination.encode('utf-8')).hexdigest()
        archive_path = os.path.join(self.archive_directory, archive_key)
        if not os.path.isfile(archive_path):
            self.downloader.download(application, archive_path)
        shutil.copy(archive_path, destination)
