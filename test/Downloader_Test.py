# -*- coding: utf-8 -*-
import unittest
from applications import Downloader
from applications import keepass
from os import path
from unittest import TestCase


class ApplicationsHomeTest(TestCase):
    downloader = Downloader()

    def test_download_from_sourceforge(self):
        self.downloader.download(keepass(), path.expanduser("~/tmp/keePass.zip"))

if __name__ == '__main__':
    unittest.main()
