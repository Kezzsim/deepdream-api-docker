Deep Dream API server Container
====================

This is an example Deep Dream container that runs https://github.com/google/deepdream in an API that can be run on compute resources provided by https://runpod.io
https://github.com/runpod/runpod-python
For now this furnishes a runpod endpoint style api which accepts JSON files containing a link to a valid .jpg image, processes said image using GPU compute, and returns an deep dream style image as a response. Additional arguments are also accepted via JSON.

![Example image showing the HTML 5 form for making a deepDream request](https://raw.githubusercontent.com/Kezzsim/deepdream-api-docker/master/example.png)

This is not an official Google product.
The goal of this project is to provide an easy to run deepDream image for nostalgia and preservation purpouses.

#### Uses Imgur to host completed pictures : https://apidocs.imgur.com/
This container relies on https://github.com/kesara/deepdreamer for porting DeepDream to python3.

#### TODO:
- [x] POST JSON REST API at `/`
- [ ] Add parameters from JSON request
- [ ] Automatically transcode files to compatible types (only JPG is supported currently.)
- [ ] Asynchronous request / response mode
- [ ] Animation support
- [ ] Multiple dreams

Setting Env Variables
----------------------
1. RUNPOD_API_KEY = your [runpod API key](https://www.runpod.io/console/serverless/user/settings)
2. IMGURCLIENT_ID
3. IMGURCLIENT_SECRET
Building the Container
----------------------
Nothing special if you already have Docker installed:

    $ git clone --branch runpod https://github.com/Kezzsim/deepdream-api-docker.git
    $ cd deepdream-api-docker
    $ docker build -t deepdream-api-runpod .
Running the Container
---------------------
To run this container:

    $ docker run -p 8080:5000 -it deepdream-api-runpod
    
