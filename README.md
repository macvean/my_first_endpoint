# Manage your API with Google Cloud Endpoints - Python & GKE

##This Series
This tutorial is the first of many in a series. By following all parts, you will incrementaly build a fully fledged web API, incorporating many of the core features and capabilities of Google Cloud Endpoints. The tutorials are as follows:

1. Part One - Your First Endpoint (you are here)
2. Part Two - Updating your API
3. Part Three - Securing your API - API Keys
4. Part Four - oAuth based API Access
5. Part Five - Sharing your API with other Users

Although each part incrementally builds upon the earlier parts, you should be able to dive straight into a future tutorial if you have a particular subject you are interested in learning. 

Okay, without further adieu, let's build and manage our first API with Google Cloud Endpoints. 

#Part One - Your first Endpoint

##Welcome
###Goal of this Tutorial
**Build, deploy, and test a simple 'hello world' API using Python, Flask, Google Container Engine and Google Cloud Endpoints.**

###Files included in this tutorial:

1. **my_first_endpoint.py** - A Python + Flask API backend.
2. **swagger.yaml** - An OpenAPI specification for your API.
3. **my_first_endpoints_GKE.yaml** - Configuration file to set-up your system. Most critically, it contains instructions for both your API container, and the Endponints Server Proxy container which will handle API management.
4. **Dockerfile** - Instructions for building the container image for your API.
5. **requirements.txt** - The Python libraries to be installed in your container image.

###API Overview

Our backend will be a simple Python + Flask application. The application will be run using Google Container Enigne. We will use Google Cloud Endpoints for its API management capabilities (which we will gradually add over the course of future tutorials).

Our API will have two methods: 
1. 'hello' which will return the text 'Hello Endpoints'.
2. 'reverse' which will take a given string and reverse it. 

###Assumptions
This tutorial is designed to get you up and running with your first Google Cloud Endpoints API. Thus, while we will try to go slowly through each and every stage in the process, this is not a general Google Cloud Platform (GCP) or Google Container Enginer (GKE) tutorial. If you need help getting set up with GCP, please read the official getting started guides.

Likewise, if you are new to Python or Flask, this might not be the tutorial for you. Or maybe it will be, because we will try to go easy.

We assume you are working with Python 2.7, as the code is written using 2.7. All core concepts apply across versions (and indeed languages), but the code supplied is only tested with 2.7

###Prerequisites

1. You have a Google Cloud Platform project, with billing enabled.
2. You have Python 2.7 installed.
3. You have the Cloud SDK installed.
4. You have cURL installed.
5. You have pip installed.
6. You have virtualenv installed.

##Your API Backend

Before we go through the process of defining, deploying, and testing our API, here is what the backend looks like:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
	return "Hello Endpoints"

@app.route("/reverse/<input_string>", methods=['GET'])
def reverse(input_string):
	reversed_string = input_string[::-1]
	return reversed_string

if __name__ == "__main__":
    app.run()
```

We are not going to closely comment on the backend, given the simplicity of the design. This should look like a standard Python + Flask application. Nothing special is required here to work successfully with Google Cloud Endpoints.

##Swagger Spec
In order to manage our API with Google Cloud Endpoints, we must provide a specification for it using the OpenAPI Specification framework (Swagger). This allows the Endpoints proxy to appropriately manage and monitor the requests to your API, allowing for all the core features of Endpoints such as authentication, usage monitoring, and logging. 

Before explaining what is happening here, this is what our swagger spec will look like for our simple Endpoints API.

##Getting Google Container Engine Ready
Project prerequisites reminder:

1. You have create a Google Cloud Platform project, it has billing enabled, and you know the project ID.
2. You have installed the Cloud SDK.
3. You have installed Docker.

Ensure you are autheticated into the Cloud SDK, and you have set the SDK config to point to the correct project

```
gcloud auth login
```

```
gcloud config set project [YOUR PROJECT ID]
```

Create your cluster:
```
gcloud container clusters create api-cluster
```

Build your docker image from the Dockerfile attached

```
docker build -f /path/to/your/Dockerfile .
```

Tag your newly created image:

```
docker tag [YOUR IMAGE ID] gcr.io/[YOUR PROJECT ID]/endpoints-image
```

And now push the image to Google Container Registry

```
gcloud docker push gcr.io/[YOUR PROJECT ID]/endpoints-image
```

##Deploying Your API

##Testing Your API

##Viewing the Endpoints GUI

##Next Episode
