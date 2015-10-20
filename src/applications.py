# -*- coding: utf-8 -*-
from os.path import expanduser
from os.path import join
import os
import errno
import tarfile
import urlparse
import sys

import requests


def _search_path_for(pathname_suffix):
    candidates = [os.path.join(directory, pathname_suffix) for directory in sys.path]
    try:
        return filter(os.path.exists, candidates)[0]
    except IndexError:
        return None


class ApplicationsHome:
    def __init__(self, path):
        self.path = expanduser(path)
        self.configuration_path = os.path.join(self.path, "etc")

    def ensure_exists(self):
        mkdir_p(self.path)
        mkdir_p(self.configuration_path)
        self._write_rc_file()

    def install(self, application):
        self._ensure_installation_directory_exists(application)
        self._ensure_archive_was_downloaded(application)
        self._extract_archive(application)

        path = application.metadata_for('path')
        if path is not None:
            path_to_path_file = os.path.join(self.configuration_path, application.name + '.path')
            with open(path_to_path_file, 'wb') as path_file:
                path_file.write(path % self._template_data_for(application))

        env = application.metadata_for('env')
        if env is not None:
            path_to_env_file = os.path.join(self.configuration_path, application.name + '.env')
            with open(path_to_env_file, 'wb') as env_file:
                template_content = '\n'.join(map(lambda (key, value): key + '="' + value + '"', env.items()))
                env_file.write(template_content % self._template_data_for(application))

    def _write_rc_file(self):
        path_to_rc_script = _search_path_for('shell/application.sh')
        with open(path_to_rc_script, 'r') as rc_file:
            rc_file_template = rc_file.read()
        path_to_destination = os.path.join(self.path, 'application.rc')
        with open(path_to_destination, 'w')as rc_file_installed:
            replacement = "application_directory='%(path)s'" % {'path': self.path}
            rc_file_installed.write(rc_file_template.replace("application_directory='/tmp'", replacement))

    def _template_data_for(self, application):
        return {'installation_directory': self._directory_for(application)}

    def _ensure_installation_directory_exists(self, application):
        mkdir_p(self._parent_directory_for(application))

    def _ensure_archive_was_downloaded(self, application):
        if self._archive_already_downloaded(application):
            print 'already downloaded ' + application.filename()
            return

        print(application.url())
        response = requests.get(application.url(), stream=True)
        print response.status_code
        with open(self._archive_path_for(application), "wb") as storage_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    storage_file.write(chunk)
                    storage_file.flush()

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
        return os.path.join(self.path, application.name)

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
    def __init__(self, name, version, url_template, metadata=None):
        self.name = name
        self.version = version
        self.url_template = url_template
        self.metadata = metadata if metadata else {}

    def filename(self):
        parsed_url = urlparse.urlparse(self.url())
        filename = os.path.basename(parsed_url.path)
        return filename

    def url(self):
        return self.url_template % {'version': self.version}

    def metadata_for(self, key):
        return self.metadata.get(key)


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
    installationDirectory = ApplicationsHome(expanduser('~/apps/'))
    installationDirectory.ensure_exists()

    java_mirror = 'http://dl.dropboxusercontent.com/u/176191/boxen'
    java_mirror = 'http://localhost:8080/files'
    java_download_url_template = java_mirror = java_mirror + '/java/jdk-%(version)s-linux-x64.tar.gz'

    java_metadata = {
        'path': '%(installation_directory)s/bin',
        'env': {
            'JAVA_HOME': '%(installation_directory)s'
        }
    }
    #installationDirectory.install(Application('java', '8u40', java_download_url_template, java_metadata))

    maven_mirror = 'http://artfiles.org/apache.org'
    #maven_mirror = 'http://localhost:8080/files/apache'
    maven_download_url_template = maven_mirror + '/maven/maven-3/%(version)s/binaries/apache-maven-%(version)s-bin.tar.gz'

    maven_metadata = {
        'path': '%(installation_directory)s/bin'
    }
    installationDirectory.install(Application('maven', '3.3.3', maven_download_url_template, maven_metadata))

    jetbrains_mirror = 'http://download.jetbrains.com'
    #jetbrains_mirror = 'http://localhost:8080/files/jetbrains'

    idea_download_url_template = jetbrains_mirror + '/idea/ideaIU-%(version).tar.gz'
    #installationDirectory.install(Application('idea', '14.0.4', idea_download_url_template))
    installationDirectory.install(Application('idea', '14.1.5', idea_download_url_template))

    xmind_mirror = 'http://www.xmind.net'
    xmind_download_url_template = xmind_mirror + '/xmind/downloads/xmind-portable-3.5.1.201411201906.zip'
    # installationDirectory.install(Application('xmind', '3.5.1', xmind_download_url_template))
