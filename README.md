This is a simple html auto-reloading/auto-refreshing demo.

It auto reloads HTML content created by a simple python backend (see [sample_backend.py](./sample_backend.py)).

Tested on Python 3.7.


# Simple Demos

To run:


* Install bottle:

        pip3 install bottle

* Run the server:

        python bottle_server.py

* Enjoy: <http://localhost:8989/>

# Websockets Demo (asyncio & aiohttp)

To run:


* Install aiohttp:

        pip3 install aiohttp

* Run the server:

        python websockets_server.py

* Enjoy: <http://localhost:8080/>

# Websockets Demo (pubsub & requests)

This demo launches a websocket based pubsub server which allows pushing new content via websockets while using regular python code (without asyncio).   To run:


* Install aiohttp:

        pip3 install aiohttp

* Run the pubsubserver:

        python websockets_pubsub.py

* Connect subscribers (signs) via: <http://localhost:8080/>

* POST to http://localhost:8080/publish/ to post new content.  For a demo refer to [publish.py](./publish.py):

        python publish.py
