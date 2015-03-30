from hamcrest import *
from unittest import TestCase
import unittest
from applications import Application


class ApplicationsHomeTest(TestCase):
    application = Application("do_not_care", '1.2.3', 'http://example.org/artifact-%(version)s')

    def test_replace_version_in_url(self):
        assert_that(self.application.url(), all_of(
            contains_string('1.2.3'),
            not_(contains_string('%(version)s'))))

    def test_replace_version_in_filename(self):
        assert_that(self.application.filename(), all_of(
            contains_string('1.2.3'),
            not_(contains_string('%(version)s'))))

if __name__ == '__main__':
    unittest.main()
