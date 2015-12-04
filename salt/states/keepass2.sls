add-KeePass2-ppa:
  pkgrepo.managed:
    - humanname: KeePass 2 PPA
    - name: ppa:jtaylor/keepass
    - file: /etc/apt/sources.list.d/KeePass2.list
    - keyid: 58B80F90
    - keyserver: keyserver.ubuntu.com

install-KeePass2:
  pkg:
    - name: keepass2
    - installed
    - allow_updates: True
    - require:
      - pkgrepo: add-KeePass2-ppa