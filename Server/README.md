# Containerisation for local development

In this folder, `Dockerfile` runs the Flask Server in a container.

The `docker-compose.yml` defines a cluster with the Server and a local PG container

For convenience, a Makefile supports the following simple operations:

* `make build` builds an image from the current working copy
* `make run` starts the cluster, rebuilding if necessary
* `make logs` tails the logs for both containers
* `make stop` stops and deletes the clusters

## Prerequisites

You will need to have a Docker environment available... Docker Desktop or an equivalent

## Previous Issues

### ThirdWeb

The build step (`make build`) fails whilst running `pipenv install` during the build of the Docker image.

`thirdweb-sdk` caused errors on `pipenv install`. The output was long and ugly; no resolution has been found, so we are removing this for now.

### Ventura - Flask default port 5000

Flask runs by default on port 5000.  However, on macos Ventura, there is a system service "Airplay Receiver" listening on this port.

In this case, `localhost:5000` does not reach the Flask app, although `127.0.0.1:5000` does.

The easiest solution is to turn off the Airplay Receiver service; an alternative is to run Flask on a different port... perhaps 7355 for TESS?

[Here's a full discussion of the issue](https://blog.yimingliu.com/2023/01/01/cannot-connect-to-flask-development-server-on-localhost-port-5000/).

## Current Issue

The server (running in docker compose) reports an ImportError:

```
zen-server-1    | Error: While importing 'app', an ImportError was raised:
sytizen-server-1    | 
sytizen-server-1    | Traceback (most recent call last):
sytizen-server-1    |   File "/usr/local/lib/python3.9/site-packages/flask/cli.py", line 218, in locate_app
sytizen-server-1    |     __import__(module_name)
sytizen-server-1    |   File "/app/app.py", line 15, in <module>
sytizen-server-1    |     from ansible.tic_classify import tic_classify
sytizen-server-1    |   File "/app/ansible/tic_classify.py", line 2, in <module>
sytizen-server-1    |     from thirdweb import ThirdwebSDK
sytizen-server-1    | ModuleNotFoundError: No module named 'thirdweb'
```