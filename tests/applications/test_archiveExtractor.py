from unittest import TestCase

from applications.extractor import ArchiveExtractor
from hamcrest import *


class TestArchiveExtractor(TestCase):
    def test_drop_zero_returns_path(self):
        download_path = ArchiveExtractor()._archive_path_to_extract_path('some/path', 0)
        assert_that(download_path, equal_to('some/path'))

    def test_remove_the_number_of_parents_passed(self):
        download_path = ArchiveExtractor()._archive_path_to_extract_path('some/path', 1)
        assert_that(download_path, equal_to('path'))

    def test_remove_the_number_of_parents_passed_two(self):
        download_path = ArchiveExtractor()._archive_path_to_extract_path('some/deep/path/path/', 3)
        assert_that(download_path, equal_to('path'))

    def test_return_empty_string_if_no_path_element_remains(self):
        download_path = ArchiveExtractor()._archive_path_to_extract_path('some', 1)
        assert_that(download_path, equal_to(''))
