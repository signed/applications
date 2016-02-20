import errno
import sys
import urlparse

import applications.downloader
import applications.extractor
import os
from abc import abstractmethod, ABCMeta
from os.path import expanduser
from os.path import join


def create():
    download_cache_directory = os.path.join(os.getcwd(), 'downloads')
    mkdir_p(download_cache_directory)

    combined_downloader = applications.downloader.ArchivingDownloader(download_cache_directory,
                                                                      applications.downloader.Downloader())
    return ApplicationInstaller(expanduser('~/apps/'), combined_downloader)


def _search_path_for(pathname_suffix):
    candidates = [os.path.join(directory, pathname_suffix) for directory in sys.path]
    try:
        return filter(os.path.exists, candidates)[0]
    except IndexError:
        return None


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


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


class InstallationStep(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def install(self, directory_structure, application, template_data): pass


class FileWriter:
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def write_to(self, path, mode, content):
        with open(path, mode) as output_file:
            output_file.write(content)


class WriteEnvironmentVariableFile(InstallationStep):
    def install(self, directory_structure, application, template_data):
        env = application.metadata_for('env')
        if env is None:
            return
        path_to_env_file = os.path.join(directory_structure.configuration_path, application.name + '.env')

        lines = []
        for key, value in env.items() :
            lines.append(key + '="' + value + '"')

        content_with_template_variables = '\n'.join(lines)
        print(content_with_template_variables)
        content = content_with_template_variables % template_data
        FileWriter().write_to(path_to_env_file, 'wt', content)


class WritePathAdditionFile(InstallationStep):
    def install(self, directory_structure, application, template_data):
        path = application.metadata_for('path')
        if path is not None:
            path_to_path_file = os.path.join(directory_structure.configuration_path, application.name + '.path')
            with open(path_to_path_file, 'wt') as path_file:
                path_file.write(path % template_data)


class PointCurrentSymLinkToApplication(InstallationStep):
    def install(self, directory_structure, application, template_data):
        current_sym_link = directory_structure.current_symlink_path_for(application)

        if os.path.islink(current_sym_link):
            os.unlink(current_sym_link)

        extract_directory = directory_structure.directory_for(application)
        os.symlink(extract_directory + '/', current_sym_link)


class ApplicationInstaller:
    def __init__(self, path, downloader):
        self.directory_structure = DirectoryStructure(expanduser(path))
        self.downloader = downloader

    def ensure_environment_is_setup(self):
        self.directory_structure.ensure_directories_are_setup()
        self._write_rc_file()

    def install(self, application):
        template_data = self._template_data_for(application)
        self.directory_structure.ensure_installation_directory_exists(application)
        self._ensure_archive_was_downloaded(application)
        self._extract_archive(application)
        PointCurrentSymLinkToApplication().install(self.directory_structure, application, template_data)
        WritePathAdditionFile().install(self.directory_structure, application, template_data)
        WriteEnvironmentVariableFile().install(self.directory_structure, application, template_data)

    def _write_rc_file(self):
        path_to_rc_script = _search_path_for('shell/application.sh')
        with open(path_to_rc_script, 'r') as rc_file:
            rc_file_template = rc_file.read()
        path_to_destination = os.path.join(self.directory_structure.path, 'application.rc')
        with open(path_to_destination, 'w')as rc_file_installed:
            replacement = "application_directory='%(path)s'" % {'path': self.directory_structure.path}
            rc_file_installed.write(rc_file_template.replace("application_directory='/tmp'", replacement))

    def _ensure_archive_was_downloaded(self, application):
        self.downloader.download(application, self.directory_structure.archive_path_for(application))

    def _template_data_for(self, application):
        return {'installation_directory': self.directory_structure.current_symlink_path_for(application)}

    def _extract_archive(self, application):
        if self.directory_structure.archive_already_extracted(application):
            print('already extracted ' + application.filename())
            return

        archive_path = self.directory_structure.archive_path_for(application)
        target_directory_path = self.directory_structure.directory_for(application)

        applications.extractor.ArchiveExtractor().extract(archive_path, target_directory_path)


class DirectoryStructure:
    def __init__(self, path):
        self.path = path
        self.configuration_path = os.path.join(self.path, "etc")

    def ensure_directories_are_setup(self):
        mkdir_p(self.path)
        mkdir_p(self.configuration_path)

    def ensure_installation_directory_exists(self, application):
        mkdir_p(self._parent_directory_for(application))

    def current_symlink_path_for(self, application):
        return join(self._parent_directory_for(application), 'current')

    def archive_path_for(self, application):
        return join(self._parent_directory_for(application), application.filename())

    def directory_for(self, application):
        return os.path.join(self._parent_directory_for(application), application.version)

    def archive_already_extracted(self, application):
        return os.path.isdir(self.directory_for(application))

    def _parent_directory_for(self, application):
        return os.path.join(self.path, application.name)
