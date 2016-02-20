import unittest
from unittest import TestCase


class ApplicationsHomeTest(TestCase):
    def test_replace_version_in_url(self):
        prep = ['%(installation_directory)s/' + x for x in ['bin', 'src']]
        print(prep)

    def test_dictionary_iteration(self):
        dictionary = {
            'one': 1,
            'two': 2
        }
        for k, v in dictionary.iteritems():
            print k, v


if __name__ == '__main__':
    unittest.main()
