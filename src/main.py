# -*- coding: utf-8 -*-
import applications.downloader
import applications.extractor
import applications.installer
from applications.installer import Application


def maven():
    name = 'maven'
    version = '3.3.3'
    url = 'http://artfiles.org/apache.org/maven/maven-3/%(version)s/binaries/apache-maven-%(version)s-bin.tar.gz'
    metadata = {
        'path': '%(installation_directory)s/bin'
    }
    return Application(name, version, url, metadata)


def oracle_java():
    name = 'java'
    version = '8u40'
    url = 'http://dl.dropboxusercontent.com/u/176191/boxen/java/jdk-%(version)s-linux-x64.tar.gz'
    metadata = {
        'path': '%(installation_directory)s/bin',
        'env': {
            'JAVA_HOME': '%(installation_directory)s'
        }
    }
    return Application(name, version, url, metadata)


def intellij():
    name = 'idea'
    version = '15.0.1'
    url = 'http://download.jetbrains.com/idea/ideaIU-%(version)s.tar.gz'
    metadata = {
        'path': '%(installation_directory)s/bin'
    }
    return Application(name, version, url, metadata)


def xmind():
    name = 'xmind'
    version = '3.5.1'
    url = 'http://www.xmind.net/xmind/downloads/xmind-portable-3.5.1.201411201906.zip'
    return Application(name, version, url)


if __name__ == '__main__':
    applicationInstaller = applications.installer.create()
    applicationInstaller.ensure_environment_is_setup()

    applicationInstaller.install(oracle_java())
    # applications.install(maven())
    # applications.install(intellij())
    # applications.install(xmind())
