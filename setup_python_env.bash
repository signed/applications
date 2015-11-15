#!/bin/bash

script_dir=`pwd`
python_3_5_base_directory=${script_dir}/downloads/python-3.5.0-bin

#compile python 3.5
if [ ! -d "${python_3_5_base_directory}" ]; then
    mkdir -p downloads
    pushd downloads
    curl -O https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tar.xz
    unxz Python-3.5.0.tar.xz
    tar xvf Python-3.5.0.tar
    cd Python-3.5.0

    ./configure --prefix=${python_3_5_base_directory}
    make
    make install
    popd
fi

virtual_environment=${script_dir}/environment/virtualenv
if [ ! -d "${virtual_environment}" ]; then
    virtualenv --python=${python_3_5_base_directory}/bin/python3.5 ${virtual_environment}
fi