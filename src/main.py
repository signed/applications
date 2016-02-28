# -*- coding: utf-8 -*-
import applications.downloader
import applications.extractor
import applications.installer
from applications.installer import Application
from applications.installer import ArchiveConfiguration
from applications.installer import EnvironmentConfiguration


def maven():
    name = 'maven'
    version = '3.3.9'

    archive = {
        'url': 'https://mirror.netcologne.de/apache.org/maven/maven-3/%(version)s/binaries/apache-maven-%(version)s-bin.tar.gz',
        'checksum': {
            'md5': '516923b3955b6035ba6b0a5b031fbd8b'
        },
        'nesting_level': 1
    }

    etc = {
        'path': '%(installation_directory)s/bin'
    }

    return Application(name, version, ArchiveConfiguration(archive), EnvironmentConfiguration(etc), etc)


def oracle_java():
    name = 'java'
    version = '8u40'

    archive = {
        'url': 'http://dl.dropboxusercontent.com/u/176191/boxen/java/jdk-%(version)s-linux-x64.tar.gz',
        'nesting_level': 1
    }

    configuration = {
        'path': '%(installation_directory)s/bin',
        'env': {
            'JAVA_HOME': '%(installation_directory)s'
        }
    }
    return Application(name, version, ArchiveConfiguration(archive), EnvironmentConfiguration(configuration), configuration)


def intellij():
    name = 'idea'
    version = '15.0.4'

    archive = {
        'url': 'http://download.jetbrains.com/idea/ideaIU-%(version)s.tar.gz',
        'nesting_level': 1
    }

    etc = {
        'path': '%(installation_directory)s/bin'
    }
    return Application(name, version, ArchiveConfiguration(archive), EnvironmentConfiguration(etc), etc)


def xmind():
    name = 'xmind'
    version = '3.5.1'

    archive = {
        'url': 'http://www.xmind.net/xmind/downloads/xmind-portable-3.5.1.201411201906.zip',
        'nesting_level': 0
    }
    etc = {
        'path': '%(installation_directory)s/XMind_Linux_64bit'
    }
    return Application(name, version, ArchiveConfiguration(archive), EnvironmentConfiguration(etc), etc)


if __name__ == '__main__':
    applicationInstaller = applications.installer.create()
    applicationInstaller.ensure_environment_is_setup()

    # applicationInstaller.install(oracle_java())
    # applicationInstaller.install(maven())
    # applicationInstaller.install(intellij())
    applicationInstaller.install(xmind())
