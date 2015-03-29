# -*- coding: utf-8 -*-
from os.path import expanduser
from os.path import join
import os
import errno
import zipfile

import requests


class ApplicationsHome:
    def __init__(self, path):
        self.path = path

    def ensure_exists(self):
        mkdir_p(self.path)
        mkdir_p(self.path+"/bin")
        pass

    def install(self, application):
        self._ensure_installation_directory_exists(application)
        self._ensure_archive_was_downloaded(application)
        self._extract_archive(application)

    def _ensure_installation_directory_exists(self, application):
        mkdir_p(self._directory_for(application))

    def _ensure_archive_was_downloaded(self, application):
        if not self._archive_already_downloaded(application):
            response = requests.get(application.url())
            print response.status_code
            print response.url

            with open(self._archive_path_for(application), "wb") as code:
                code.write(response.content)
        else:
            print 'already downloaded ' + application.filename()

    def _extract_archive(self, application):
        with zipfile.ZipFile(self._archive_path_for(application), "r") as archive:
            archive.extractall(self._directory_for(application))

    def _archive_path_for(self, application):
        return join(self._directory_for(application), application.filename())

    def _directory_for(self, application):
        data = {'base_path': self.path, 'application_name': application.name}
        target_directory = expanduser("%(base_path)s/%(application_name)s" % data)
        return target_directory

    def _archive_already_downloaded(self, application):
        return os.path.isfile(self._archive_path_for(application))


class Application:
    def __init__(self, name, version, url_template, file_name_template):
        self.name = name
        self.version = version
        self.url_template = url_template
        self.file_name_template = file_name_template

    def filename(self):
        return self.file_name_template % {'version': self.version}

    def url(self):
        return self.url_template % {'version': self.version, 'filename': self.filename()}


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if __name__ == '__main__':
    installationDirectory = ApplicationsHome(expanduser('~/applications_dev/'))
    installationDirectory.ensure_exists()
    mirror = 'http://localhost:8080/files'
    maven_download_url_template = mirror + '/apache/maven/maven-3/%(version)s/binaries/%(filename)s'
    maven_archive_template = 'apache-maven-%(version)s-bin.zip'

    installationDirectory.install(Application('maven', '3.2.5', maven_download_url_template, maven_archive_template))
    installationDirectory.install(Application('maven', '3.3.1', maven_download_url_template, maven_archive_template))



