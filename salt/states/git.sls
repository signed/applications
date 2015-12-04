install-git:
  pkg:
    - installed
    - allow_updates: True
    - name: git


install-etckeeper:
  pkg:
    - require:
      - pkg: install-git
    - installed
    - allow_updates: True
    - name: etckeeper

configure-etckeeper-to-use-git:
  file:
    - require:
      - pkg: install-etckeeper
    - uncomment
    - name: /etc/etckeeper/etckeeper.conf
    - regex: ^VCS="git"$

configure-etckeeper-do-not-use-bzr:
  file:
    - require:
      - file: configure-etckeeper-to-use-git
    - comment
    - name: /etc/etckeeper/etckeeper.conf
    - regex: ^VCS="bzr"$

initialze-etckeeper-repository:
  cmd:
    - require:
      - file: configure-etckeeper-do-not-use-bzr
    - run
    - name: etckeeper init && etckeeper commit 'initial commit'
    - unless: test -d /etc/.git