# -*- coding: utf-8 -*-
import tarfile
import zipfile
import string
import shutil
from zipfile import ZipInfo

import os
from pathlib2 import PurePath


class ArchiveExtractor:
    def __init__(self):
        pass

    def extract(self, archive_path, target_directory_path, nesting_depth):
        if tarfile.is_tarfile(archive_path):
            with _MyHackedTarFile.open(archive_path, 'r') as tar:
                for tarinfo in tar.getmembers():
                    destination = os.path.join(target_directory_path, self._archive_path_to_extract_path(tarinfo.path, nesting_depth))
                    tar.extract_member_to(tarinfo, destination)
        elif zipfile.is_zipfile(archive_path):
            # with zipfile.ZipFile(archive_path, 'r') as zip_file:
            with _MyHackedZipFile(archive_path, 'r') as zip_file:
                for archive_path in zip_file.namelist():
                    destination = os.path.join(target_directory_path, self._archive_path_to_extract_path(archive_path, nesting_depth))
                    zip_file.extract_member_to(archive_path, destination)
        else:
            archive_name = os.path.basename(archive_path)
            raise ValueError("Unsupported archive type " + archive_name)

    def _archive_path_to_extract_path(self, archive_path, number_of_parents_to_drop):
        path_elements = PurePath(archive_path).parts[number_of_parents_to_drop:]
        if not path_elements:
            return ''
        return os.path.join(os.path.join(*path_elements))


class _MyHackedTarFile(tarfile.TarFile):
    def extract_member_to(self, member, path=""):
        self._check("r")

        if isinstance(member, str):
            tarinfo = self.getmember(member)
        else:
            tarinfo = member

        # Prepare the link target for makelink().
        if tarinfo.islnk():
            tarinfo._link_target = os.path.join(path, tarinfo.linkname)

        try:
            self._extract_member(tarinfo, path)
        except OSError as e:
            if self.errorlevel > 0:
                raise
            else:
                if e.filename is None:
                    self._dbg(1, "tarfile: %s" % e.strerror)
                else:
                    self._dbg(1, "tarfile: %s %r" % (e.strerror, e.filename))
        except tarfile.ExtractError as e:
            if self.errorlevel > 1:
                raise
            else:
                self._dbg(1, "tarfile: %s" % e)


class _MyHackedZipFile(zipfile.ZipFile):
    def extract_member_to(self, member, targetpath, pwd=None):
        """Extract the ZipInfo object 'member' to a physical
           file on the path targetpath.
        """
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        # build the destination pathname, replacing
        # forward slashes to platform specific separators.
        arcname = member.filename.replace('/', os.path.sep)

        if os.path.altsep:
            arcname = arcname.replace(os.path.altsep, os.path.sep)
        # interpret absolute pathname as relative, remove drive letter or
        # UNC path, redundant separators, "." and ".." components.
        arcname = os.path.splitdrive(arcname)[1]
        arcname = os.path.sep.join(x for x in arcname.split(os.path.sep)
                                   if x not in ('', os.path.curdir, os.path.pardir))
        if os.path.sep == '\\':
            # filter illegal characters on Windows
            illegal = ':<>|"?*'
            if isinstance(arcname, unicode):
                table = {ord(c): ord('_') for c in illegal}
            else:
                table = string.maketrans(illegal, '_' * len(illegal))
            arcname = arcname.translate(table)
            # remove trailing dots
            arcname = (x.rstrip('.') for x in arcname.split(os.path.sep))
            arcname = os.path.sep.join(x for x in arcname if x)

        targetpath = os.path.normpath(targetpath)

        # Create all upper directories if necessary.
        upperdirs = os.path.dirname(targetpath)
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs)

        if member.filename[-1] == '/':
            if not os.path.isdir(targetpath):
                os.mkdir(targetpath)
            return targetpath

        with self.open(member, pwd=pwd) as source, \
                file(targetpath, "wb") as target:
            shutil.copyfileobj(source, target)

        return targetpath
