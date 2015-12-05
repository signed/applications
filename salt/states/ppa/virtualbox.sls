add virtualbox package repository:
  pkgrepo.managed:
    - name: deb http://download.virtualbox.org/virtualbox/debian {{ grains["oscodename"] }} contrib
    - humanname: {{ grains["os"] }} {{ grains["oscodename"]|capitalize }} VirtualBox Package Repository
    - key_url: https://www.virtualbox.org/download/oracle_vbox.asc
    - file: /etc/apt/sources.list.d/virtualbox.list
    - refresh_db: True

install virtualbox:
  pkg.latest:
    - require:
      - pkgrepo: add virtualbox package repository
    - name: virtualbox-5.0
    - refresh: True

install dkms:
  pkg.latest:
    - require:
      - pkg: virtualbox-5.0
    - name: dkms