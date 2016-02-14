from hamcrest import *
from unittest import TestCase
import unittest

class ApplicationsHomeTest(TestCase):

    def test_replace_version_in_url(self):
        prep = ['%(installation_directory)s/'+x for x in ['bin', 'src']]
        print(prep)

if __name__ == '__main__':
    unittest.main()
