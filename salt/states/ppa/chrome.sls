add-google-chrome-ppa:
  pkgrepo:
    - managed
    - humanname: Google Chrome
    - name: deb http://dl.google.com/linux/chrome/deb/ stable main
    - dist: stable
    - file: /etc/apt/sources.list.d/google-chrome.list
    - gpgcheck: 1
    - key_url: https://dl-ssl.google.com/linux/linux_signing_key.pub

install-google-chrome:
  pkg:
    - require:
      - pkgrepo: add-google-chrome-ppa
    - name: google-chrome-stable
    - installed
    - allow_updates: True
