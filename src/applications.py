# -*- coding: utf-8 -*-
from os.path import expanduser
from os.path import join
import os
import errno
import tarfile

import requests


class ApplicationsHome:
    def __init__(self, path):
        self.path = expanduser(path)

    def ensure_exists(self):
        mkdir_p(self.path)
        mkdir_p(self.path + "/bin")
        pass

    def install(self, application):
        self._ensure_installation_directory_exists(application)
        self._ensure_archive_was_downloaded(application)
        self._extract_archive(application)

    def _ensure_installation_directory_exists(self, application):
        mkdir_p(self._parent_directory_for(application))

    def _ensure_archive_was_downloaded(self, application):
        if not self._archive_already_downloaded(application):
            print(application.url())
            response = requests.get(application.url())
            print response.status_code
            print response.url

            with open(self._archive_path_for(application), "wb") as code:
                code.write(response.content)
        else:
            print 'already downloaded ' + application.filename()

    def _extract_archive(self, application):
        if self._archive_already_extracted(application):
            print 'already extracted ' + application.filename()
            return

        archive_path = self._archive_path_for(application)
        target_directory_path = self._directory_for(application)

        ArchiveExtractor().extract(archive_path, target_directory_path)

    def _archive_path_for(self, application):
        return join(self._parent_directory_for(application), application.filename())

    def _parent_directory_for(self, application):
        data = {'base_path': self.path, 'application_name': application.name}
        target_directory = os.path.join(self.path, application.name)
        return target_directory

    def _directory_for(self, application):
        return os.path.join(self._parent_directory_for(application), application.version)

    def _archive_already_downloaded(self, application):
        return os.path.isfile(self._archive_path_for(application))

    def _archive_already_extracted(self, application):
        return os.path.isdir(self._directory_for(application))


class ArchiveExtractor:
    def __init__(self):
        pass

    def extract(self, archive_path, target_directory_path):
        archive_name = os.path.basename(archive_path)
        parent_directory = os.path.split(target_directory_path)[0]
        target_directory_name = os.path.basename(target_directory_path)

        if archive_path.endswith('.tar.gz'):
            with tarfile.open(archive_path, 'r') as tar:
                for tarinfo in tar.getmembers():
                    path_elements = split_path(tarinfo.path)
                    path_elements[0] = target_directory_name
                    destination = os.path.join(parent_directory, os.path.join(*path_elements))
                    tar.extract(tarinfo, destination)
        else:
            raise ValueError("Unsupported archive type" + archive_name)


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


def split_path(p):
    a, b = os.path.split(p)
    return (split_path(a) if len(a) and len(b) else []) + [b]


if __name__ == '__main__':
    installationDirectory = ApplicationsHome(expanduser('~/applications_dev/'))
    installationDirectory.ensure_exists()

    maven_mirror = 'http://artfiles.org/apache.org'
    maven_mirror = 'http://localhost:8080/files/apache'
    maven_archive_template = 'apache-maven-%(version)s-bin.tar.gz'
    maven_download_url_template = maven_mirror + '/' + 'maven/maven-3/%(version)s/binaries/%(filename)s'

    installationDirectory.install(Application('maven', '3.2.5', maven_download_url_template, maven_archive_template))
    installationDirectory.install(Application('maven', '3.3.1', maven_download_url_template, maven_archive_template))

    jetbrains_mirror = 'http://download.jetbrains.com'
    jetbrains_mirror = 'http://localhost:8080/files/jetbrains'

    idea_archive_template = 'ideaIU-%(version)s.tar.gz'
    idea_download_url_template = jetbrains_mirror + "/" + 'idea/%(filename)s'
    installationDirectory.install(Application('idea', '14.0.4', idea_download_url_template, idea_archive_template))
    installationDirectory.install(Application('idea', '14.1', idea_download_url_template, idea_archive_template))




