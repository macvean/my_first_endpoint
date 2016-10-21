# Manage your API with Google Cloud Endpoints - Python & GKE

#Part One - Your first Endpoint

##Welcome

##This Series
1. Part One - Your First Endpoint
2. Part Two - Updating your API
3. Part Three - Securing your API - API Keys
4. Part Four - oAuth based API Access
5. Part Five - Sharing your API with other Users

If you are interested in jumping directly to a future tutorial, the following tutorials are included in this series. Please note, while the tutorials are designed to build upon one another in a linear fashion, all required materials are provided with each seperate tutorial, allowing you should be able to dive straight in if you are interested in a particular topic.

##Part One - Your First Endpoint

###Goal of Tutorial
**Build, deploy, and test a simple 'hello world' API using Python, Flask, Google Container Engine and Google Cloud Endpoints.**

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

###Your API Backend

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

###Swagger Spec
In order to manage our API with Google Cloud Endpoints, we must provide a specification for it using the OpenAPI Specification framework (Swagger). This allows the Endpoints proxy to appropriately manage and monitor the requests to your API, allowing for all the core features of Endpoints such as authentication, usage monitoring, and logging. 

Before explaining what is happening here, this is what our swagger spec will look like for our simple Endpoints API.

###Deploying Your API

###Testing Your API

###Viewing the Endpoints GUI

###Next Episode
