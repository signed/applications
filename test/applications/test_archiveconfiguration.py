from unittest import TestCase

from applications.installer import ArchiveConfiguration
from hamcrest import *


class TestArchiveConfiguration(TestCase):

    dictionary = {}

    def test_get_url(self):
        self.dictionary['url'] = 'http://example.org/archive.zip'
        assert_that(self.configuration().url(), equal_to('http://example.org/archive.zip'))

    def test_get_nesting_level(self):
        self.dictionary['nesting_level'] = 5
        assert_that(self.configuration().nesting_level(), equal_to(5))

    def test_default_nesting_level_is_zero(self):
        assert_that(self.configuration().nesting_level(), equal_to(0))

    def configuration(self):
        return ArchiveConfiguration(self.dictionary)