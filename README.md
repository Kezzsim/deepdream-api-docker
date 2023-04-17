Deep Dream API server Container
====================

This is an example Deep Dream container that runs https://github.com/google/deepdream in API mode.
For now this furnishes an RESTful HTTP API that allows you to POST an image to `/` and recieve a deep dream image in return. Performing a GET request will return an HTML form that can be filled out to send requests in the browser.

![Example image showing the HTML 5 form for making a deepDream request](https://raw.githubusercontent.com/Kezzsim/deepdream-api-docker/master/example.png)

This example assumes you know how to run Docker.

This is not an official Google product.
The goal of this project is to provide an easy to run deepDream image for nostalgia and preservation purpouses.
Other projects like this repository this forks from use Python 2 which has been depricated.

This container relies on https://github.com/kesara/deepdreamer 

#### TODO:
- [x] POST REST API at `/`
- [x] HTML form response on GET that returns upload form
- [x] Add parameters to HTML form and request
- [ ] Automatically transcode files to compatible types (only JPG is supported currently.)
- [ ] Asynchronous request / response mode
- [ ] Animation support
- [ ] Multiple dreams

Running the Container
---------------------
To run this container:

    $ docker run -p 8080:5000 deepdream-api
    
Running in the Background
-------------------------

    $ docker run -p 8080:5000 -d deepdream-api
    
Find the container ID:

    $ docker container ls

Or, if the container already exited:

    $ docker ps -a | less

When you are done serving the container:

    $ docker stop {containerId}

Building the Container
----------------------
Nothing special if you already have Docker installed:

    $ git clone https://github.com/Kezzsim/deepdream-api-docker.git
    $ cd deepdream-api-docker
    $ docker build -t deepdream-api .

Connecting to the service in your browser
----------------------
`http://localhost:8080/`