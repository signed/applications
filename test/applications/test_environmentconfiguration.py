from unittest import TestCase

from applications.installer import EnvironmentConfiguration
from hamcrest import *


class TestEnvironmentConfiguration(TestCase):

    dictionary = {}

    def test_get_path(self):
        self.dictionary['path'] = 'some path'
        assert_that(self.configuration().path_element(), equal_to('some path'))

    def test_get_environment_variables(self):
        self.dictionary['env'] = {
            'One': 'one',
            'Two': 'two'
        }
        assert_that(self.configuration().environment_variables(), has_length(2))

    def configuration(self):
        return EnvironmentConfiguration(self.dictionary)