import unittest
from unittest import TestCase

from archiveinstaller.installer import ArchiveConfiguration
from archiveinstaller.installer import DirectoryStructure
from archiveinstaller.installer import EnvironmentConfiguration
from archiveinstaller.installer import FileWriter
from archiveinstaller.installer import WriteEnvironmentVariableFile
from archiveinstaller.installer import Application
from hamcrest import *
from mock import mock


class WriteEnvironmentVariableFileTest(TestCase):
    structure = DirectoryStructure("/tmp")
    name = "do_not_care"
    version = '1.2.3'
    url = 'http://example.org/artifact-%(version)s'
    metadata = {}
    template_data = {}

    @mock.patch.object(FileWriter, 'write_to')
    def test_do_nothing_if_there_are_no_environment_variables_set(self, mock_write_to):
        self.template_data = {'no_env': "some value"}
        self.execute_step()
        self.assertFalse(mock_write_to.called, "Do not try to write the env file if there are no env variables")
        assert_that(not mock_write_to.called, 'Do not try to write the env file if there are no env variables')

    @mock.patch.object(FileWriter, 'write_to')
    def test_write_existing_environment_variables_into_the_env_file(self, mock_write_to):
        self.metadata['env'] = {
            'NAME': 'VALUE'
        }
        self.execute_step()
        mock_write_to.assert_called_with('/tmp/etc/do_not_care.env', 'wt', 'NAME="VALUE"')

    def execute_step(self):
        WriteEnvironmentVariableFile().install(self.structure, self._application(), self.template_data)

    def _application(self):
        archive = {'url': self.url}

        return Application(self.name, self.version, ArchiveConfiguration(archive), EnvironmentConfiguration(self.metadata))


if __name__ == '__main__':
    unittest.main()
