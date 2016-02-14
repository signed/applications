Install Maven:
  pkg_local.installed:
    - name: maven
    - version: 3.3.9
    - url: http://artfiles.org/apache.org/maven/maven-3/%(version)s/binaries/apache-maven-%(version)s-bin.tar.gz
    - path:
        - '%(installation_directory)s/bin'

Install Oracle JDK:
  pkg_local.installed:
    - name: java
    - version: 8u40
    - url: http://dl.dropboxusercontent.com/u/176191/boxen/java/jdk-%(version)s-linux-x64.tar.gz
    - path:
        - '%(installation_directory)s/bin'
    - env:
        - JAVA_HOME: '%(installation_directory)s'

Install Intellij Ultimate:
  pkg_local.installed:
    - name: intellij
    - version: 15.0.3
    - url: http://download.jetbrains.com/idea/ideaIU-%(version)s.tar.gz
    - path:
        - '%(installation_directory)s/bin'
