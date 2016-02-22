# -*- coding: utf-8 -*-
import tarfile
import zipfile

import os
from pathlib2 import PurePath


class ArchiveExtractor:
    def __init__(self):
        pass

    def extract(self, archive_path, target_directory_path):
        if tarfile.is_tarfile(archive_path):
            with _MyHackedTarFile.open(archive_path, 'r') as tar:
                for tarinfo in tar.getmembers():
                    destination = os.path.join(target_directory_path, self._archive_path_to_extract_path(tarinfo.path, 1))
                    tar.extract_member_to(tarinfo, destination)
        elif zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for archive_path in zip_file.namelist():
                    destination = os.path.join(target_directory_path, self._archive_path_to_extract_path(archive_path, 0))
                    zip_file.extract(archive_path, destination)
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
