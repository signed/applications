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

    def already_downloaded(self, application):
        pass

    def install(self, application):
        pass


class Application:
    def __init__(self, name, version, url_template, file_name_template):
        self.name = name
        self.version = version
        self.url_template = url_template
        self.file_name_template = file_name_template

    def filename(self):
        return self.file_name_template % {'version': applicationToInstall.version}

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
    mirror = 'http://localhost:8080/files'
    maven_download_url_template = mirror + '/apache/maven/maven-3/%(version)s/binaries/%(filename)s'
    maven_archive_template = 'apache-maven-%(version)s-bin.zip'
    applicationToInstall = Application('maven', '3.2.5', maven_download_url_template, maven_archive_template)

    target_directory = expanduser(
        "~/applications_dev/%(application_name)s" % {'application_name': applicationToInstall.name})
    mkdir_p(target_directory)

    archive_file = join(target_directory, applicationToInstall.filename())

    response = requests.get(applicationToInstall.url())
    print response.status_code
    print response.url

    with open(archive_file, "wb") as code:
        code.write(response.content)

    with zipfile.ZipFile(archive_file, "r") as archive:
        archive.extractall(target_directory)




