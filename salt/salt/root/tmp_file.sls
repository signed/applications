copy stand in file to tmp directory:
  file:
    - managed
    - name: /tmp/stand_in.txt
    - source: salt://files/static_file.txt