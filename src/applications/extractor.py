# -*- coding: utf-8 -*-
import tarfile
import zipfile

import os


class ArchiveExtractor:
    def __init__(self):
        pass

    def extract(self, archive_path, target_directory_path):
        archive_name = os.path.basename(archive_path)
        parent_directory = os.path.split(target_directory_path)[0]
        target_directory_name = os.path.basename(target_directory_path)

        if tarfile.is_tarfile(archive_path):
            with _MyHackedTarFile.open(archive_path, 'r') as tar:
                for tarinfo in tar.getmembers():
                    path_elements = split_path(tarinfo.path)
                    path_elements[0] = target_directory_name
                    destination = os.path.join(parent_directory, os.path.join(*path_elements))
                    tar.extract_member_to(tarinfo, destination)
        elif zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zip:
                for name in zip.namelist():
                    destination = os.path.join(target_directory_path, name)
                    zip.extract(name, destination)
        else:
            raise ValueError("Unsupported archive type " + archive_name)


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


def split_path(p):
    a, b = os.path.split(p)
    return (split_path(a) if len(a) and len(b) else []) + [b]
