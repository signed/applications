add docker package repository:
  pkgrepo.managed:
    - name: deb https://apt.dockerproject.org/repo {{ grains["os"]|lower }}-{{ grains["oscodename"] }} main
    - humanname: {{ grains["os"] }} {{ grains["oscodename"]|capitalize }} Docker Package Repository
    - keyid: f76221572c52609d
    - keyserver: keyserver.ubuntu.com
    - file: /etc/apt/sources.list.d/docker.list
    - refresh_db: True

install docker:
  pkg.latest:
    - require:
      - pkgrepo: add docker package repository
    - name: docker-engine
    - refresh: True
