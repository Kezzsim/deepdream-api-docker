# Copyright 2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:focal

# Avoid timezone prompt
ENV TZ=America/New_York \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -q update && \
  apt-get install --no-install-recommends -y --force-yes -q \
  build-essential \
  ca-certificates \
  git \
  curl \
  python3 python3-pip 

# Install Cafe
RUN yes yes | apt-get install --force-yes -q caffe-cpu

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install runpod@git+https://github.com/Kezzsim/runpod-python.git numpy scipy pillow imgurpython

# Clone the python3 DeepDreamer repo
RUN git clone https://github.com/kesara/deepdreamer.git
WORKDIR /deepdreamer
RUN curl https://raw.githubusercontent.com/BVLC/caffe/master/models/bvlc_googlenet/deploy.prototxt -o deploy.prototxt && \
  curl http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel -o bvlc_googlenet.caffemodel

RUN echo "force_backward: true" >> deploy.prototxt

ADD deepdream.py deepdream.py
ADD test_input.json test_input.json

RUN mkdir uploads

ENTRYPOINT python3 -u ./deepdream.py
