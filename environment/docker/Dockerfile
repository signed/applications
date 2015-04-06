FROM ubuntu:14.10
MAINTAINER Thomas Heilbronner <thomas.heilbronner@gmail.com>

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python \
    python-setuptools \
    python-dev \
    python-virtualenv
RUN easy_install pip==6.0.8
RUN useradd -ms /bin/bash signed

USER signed
WORKDIR /home/signed
RUN virtualenv applications_python_environment
#RUN . applications_python_environment/bin/activate
#RUN git clone https://github.com/signed/applications.git
#WORKDIR /home/signed/applications
#RUN pip install -r requirements.txt
