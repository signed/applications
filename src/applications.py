# -*- coding: utf-8 -*-
import sys

import hashlib
import os
import requests
import shutil
import tarfile
import errno
import urlparse
import zipfile
from os.path import expanduser
from os.path import join


def _search_path_for(pathname_suffix):
    candidates = [os.path.join(directory, pathname_suffix) for directory in sys.path]
    try:
        return filter(os.path.exists, candidates)[0]
    except IndexError:
        return None


class _MyHackedTarFile(tarfile.TarFile):
    def extract_member_to(self, member, path=""):
        self._check("r")

        if isinstance(member, str):
            tarinfo = self.getmember(member)
        else:
            tarinfo = member

        # Prepare the link target for makelink().
        if tarinfo.islnk():
            tarinfo._link_target = os.path.join(path, tarinfo.linkname)

        try:
            self._extract_member(tarinfo, path)
        except OSError as e:
            if self.errorlevel > 0:
                raise
            else:
                if e.filename is None:
                    self._dbg(1, "tarfile: %s" % e.strerror)
                else:
                    self._dbg(1, "tarfile: %s %r" % (e.strerror, e.filename))
        except tarfile.ExtractError as e:
            if self.errorlevel > 1:
                raise
            else:
                self._dbg(1, "tarfile: %s" % e)


class ApplicationsHome:
    def __init__(self, path, downloader):
        self.path = expanduser(path)
        self.configuration_path = os.path.join(self.path, "etc")
        self.downloader = downloader

    def ensure_exists(self):
        mkdir_p(self.path)
        mkdir_p(self.configuration_path)
        self._write_rc_file()

    def install(self, application):
        self._ensure_installation_directory_exists(application)
        self._ensure_archive_was_downloaded(application)
        self._extract_archive(application)
        self._ensure_current_symlink_is_up_to_date(application)

        path = application.metadata_for('path')
        if path is not None:
            path_to_path_file = os.path.join(self.configuration_path, application.name + '.path')
            with open(path_to_path_file, 'wt') as path_file:
                path_file.write(path % self._template_data_for(application))

        env = application.metadata_for('env')
        if env is not None:
            path_to_env_file = os.path.join(self.configuration_path, application.name + '.env')
            with open(path_to_env_file, 'wt') as env_file:
                template_content = '\n'.join(map(lambda key, value: key + '="' + value + '"', env.items()))
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
        return {'installation_directory': self._current_symlink_path_for(application)}

    def _ensure_installation_directory_exists(self, application):
        mkdir_p(self._parent_directory_for(application))

    def _ensure_archive_was_downloaded(self, application):
        self.downloader.download(application, self._archive_path_for(application))

    def _extract_archive(self, application):
        if self._archive_already_extracted(application):
            print('already extracted ' + application.filename())
            return

        archive_path = self._archive_path_for(application)
        target_directory_path = self._directory_for(application)

        ArchiveExtractor().extract(archive_path, target_directory_path)

    def _ensure_current_symlink_is_up_to_date(self, application):
        current_sym_link = self._current_symlink_path_for(application)

        if os.path.islink(current_sym_link):
            os.unlink(current_sym_link)

        extract_directory = self._directory_for(application)
        os.symlink(extract_directory + '/', current_sym_link)

    def _current_symlink_path_for(self, application):
        return join(self._parent_directory_for(application), 'current')

    def _archive_path_for(self, application):
        return join(self._parent_directory_for(application), application.filename())

    def _parent_directory_for(self, application):
        return os.path.join(self.path, application.name)

    def _directory_for(self, application):
        return os.path.join(self._parent_directory_for(application), application.version)

    def _archive_already_extracted(self, application):
        return os.path.isdir(self._directory_for(application))


class Downloader:

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

class ArchiveExtractor:
    def __init__(self):
        pass

    def extract(self, archive_path, target_directory_path):
        archive_name = os.path.basename(archive_path)
        parent_directory = os.path.split(target_directory_path)[0]
        target_directory_name = os.path.basename(target_directory_path)

        if tarfile.is_tarfile(archive_path):
            with _MyHackedTarFile.open(archive_path, 'r') as tar:
                for tarinfo in tar.getmembers():
                    path_elements = split_path(tarinfo.path)
                    path_elements[0] = target_directory_name
                    destination = os.path.join(parent_directory, os.path.join(*path_elements))
                    tar.extract_member_to(tarinfo, destination)
        elif zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile('spam.zip', 'r') as zip:
                zip.list
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


def maven():
    url = 'http://artfiles.org/apache.org/maven/maven-3/%(version)s/binaries/apache-maven-%(version)s-bin.tar.gz'
    metadata = {
        'path': '%(installation_directory)s/bin'
    }
    return Application('maven', '3.3.3', url, metadata)


def oracle_java():
    url = 'http://dl.dropboxusercontent.com/u/176191/boxen/java/jdk-%(version)s-linux-x64.tar.gz'
    metadata = {
        'path': '%(installation_directory)s/bin',
        'env': {
            'JAVA_HOME': '%(installation_directory)s'
        }
    }
    return Application('java', '8u40', url, metadata)


def intellij():
    url = 'hdttp://download.jetbrains.com/idea/ideaIU-%(version)s.tar.gz'
    metadata = {
        'path': '%(installation_directory)s/bin'
    }
    return Application('idea', '15.0.1', url, metadata)


def xmind():
    url = 'http://www.xmind.net/xmind/downloads/xmind-portable-3.5.1.201411201906.zip'
    return Application('xmind', '3.5.1', url)


def keepass():
    url = 'http://downloads.sourceforge.net/project/keepass/KeePass 2.x/2.30/KeePass-2.30.zip'
    return Application('keepass', '2.30', url)

if __name__ == '__main__':
    download_cache_directory = os.path.join(os.getcwd(), 'downloads')
    mkdir_p(download_cache_directory)

    combined_downloader = ArchivingDownloader(download_cache_directory, Downloader())
    installationDirectory = ApplicationsHome(expanduser('~/apps/'), combined_downloader)
    installationDirectory.ensure_exists()

    # installationDirectory.install(oracle_java())
    installationDirectory.install(maven())
    # installationDirectory.install(intellij())
    # installationDirectory.install(xmind())
