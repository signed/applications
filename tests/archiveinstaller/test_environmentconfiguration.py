from unittest import TestCase

from archiveinstaller.installer import EnvironmentConfiguration
from hamcrest import *


class TestEnvironmentConfiguration(TestCase):

    def setUp(self):
        self.dictionary = {}

    def test_get_path(self):
        self.dictionary['path'] = 'some path'
        assert_that(self.configuration().path_element(), equal_to('some path'))

    def test_respond_with_none_if_there_is_nothing(self):
        assert_that(self.configuration().path_element(), equal_to(None))

    def test_get_environment_variables(self):
        self.dictionary['env'] = {
            'One': 'one',
            'Two': 'two'
        }
        assert_that(self.configuration().environment_variables(), has_length(2))

    def test_respond_with_empty_array_if_there_are_no_environment_variables(self):
        assert_that(self.configuration().environment_variables(), has_length(0))

    def configuration(self):
        return EnvironmentConfiguration(self.dictionary)
