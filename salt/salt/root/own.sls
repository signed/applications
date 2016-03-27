Install Maven:
  pkg_local.installed:
    - name: maven
    - version: 3.3.9
    - archive:
        url: http://artfiles.org/apache.org/maven/maven-3/%(version)s/binaries/apache-maven-%(version)s-bin.tar.gz
        nesting_level: 1
    - etc:
        path: '%(installation_directory)s/bin'

Install Oracle JDK:
  pkg_local.installed:
    - name: java
    - version: 8u77
    - archive:
        url: http://dl.dropboxusercontent.com/u/176191/boxen/java/jdk-%(version)s-linux-x64.tar.gz
        nesting_level: 1
    - etc:
        path: '%(installation_directory)s/bin'
        env:
            JAVA_HOME: '%(installation_directory)s'

Install Intellij Ultimate:
  pkg_local.installed:
    - name: intellij
    - version: '2016.1'
    - archive:
        url: https://download.jetbrains.com/idea/ideaIU-%(version)s.tar.gz
        nesting_level: 1
    - etc:
        path: '%(installation_directory)s/bin'

Install Xmind:
  pkg_local.installed:
    - name: xmind
    - version: 3.5.1
    - archive:
        url: http://www.xmind.net/xmind/downloads/xmind-portable-3.5.1.201411201906.zip