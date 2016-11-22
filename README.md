# Manage your API with Google Cloud Endpoints - Python & GKE

A series of tutorials to help you build and manage your first API using Google Container Enginer and Google Cloud Endpoints. This series focuses on Python and Flask.

In this first part, we build and deploy a simple Hello World API, taking you from a fresh empty project to first working API.

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
This tutorial is designed to get you up and running with your first Google Cloud Endpoints API. Thus, while we will try to go slowly through each and every stage in the process. However, this is not a general Google Cloud Platform (GCP) or Google Container Enginer (GKE) tutorial. If you need help getting set up with GCP, please read the official getting started guides.

Likewise, if you are new to Python or Flask, this might not be the tutorial for you. Or maybe it will be, because we will try to go easy.

We assume you are working with Python 2.7, as the code is written and tested with 2.7. All of the core concepts, certainly with respect to the Google Cloud Endpoints features and capabilities, apply across versions (and indeed languages), but we cannot guarantee everything will just 'work' if you are following along with a different language or version.

###Prerequisites

1. You have a Google Cloud Platform project, with billing enabled.
2. You have Python 2.7 installed.
3. You have the Cloud SDK installed.
4. You have cURL installed.
5. You have pip installed.
6. You have virtualenv installed.
7. You have flask 0.11.1 installed.

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
    app.run(host='0.0.0.0', port=8081)
```

We are not going to closely comment on the backend, given the simplicity of the design. This should look like a standard Python + Flask application. 

You can see our two methods. Hello, which will be accessed through the /hello route, will simply return our welcome message. Reverse, which will be accessed through the /reverse route, takes an input string (passed in via the URL for the API - more on this later) and returns the reversed string.

Importantly nothing special is required here for your API to work successfully with Google Cloud Endpoints, other than one thing: the port we are serving the API from. Rather than the default flask port (5000) we are running on 8081. This is due to the way the Endpoints Server Proxy (which does the API management magic) is configured by default. It will take in requests to our API and route them to port 8081.

The core message though is that this is a standard Python + Flask application.

##Swagger Spec
In order to manage our API with Google Cloud Endpoints, we must provide a specification for it using the OpenAPI Specification framework (formerly known as Swagger). This allows the Endpoints proxy to appropriately manage and monitor the requests to your backend, allowing for all the core features of Endpoints such as authentication, usage monitoring, and logging. 

Before explaining what is happening here, this is what our swagger spec will look like for our simple Endpoints API.

```
swagger: "2.0"
info:
  description: "My first Endpoints API"
  title: "Hello API"
  version: "1.0.0"
host: "YOUR PROJECT ID.appspot.com"
basePath: "/"
consumes:
- "application/json"
produces:
- "application/json"
schemes:
- "https"
paths:
  "/reverse/{input_string}":
    get:
      description: "Reverse the input string."
      operationId: "reverse"
      produces:
      - "application/json"
      responses:
        200:
          description: "Reverse"
          schema:
            type: string
      parameters:
      - description: "String to reverse"
        in: path
        name: input_string
        type: string
        required: true  
  "/hello":
    get:
      description: "A simple hello world API"
      operationId: "hello"
      produces:
      - "application/json"
      responses:
        200:
          description: "Hello"
          schema:
            type: string

```

**If you don't care about the contentes of the swagger spec, and just want to quickly run this API, all you need to do is change the 'host' line to contain your project ID. For example, host: "YOUR PROJECT ID.appspot.com" -> host: "myproject.appspot.com".**

###The Spec, Explained
**TODO: EXPLAIN EACH PART OF SWAGGER SPEC**

##Kubernetes Deployment Config at a Glance

In order to successfully deploy our API, we will be utilizing a configuration file. This ensures that the container for our API backend, and the container for the Google Cloud Endpoints API proxy (which handles the requests and does the management magic) are deployed correctly, and listening to the correct ports. 

First, this is what the config file looks like:

```
apiVersion: v1
kind: Service
metadata:
  name: first-endpoint
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: first-endpoint
  type: LoadBalancer
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: first-endpoint
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: first-endpoint
    spec:
      containers:
      - name: esp
        image: b.gcr.io/endpoints/endpoints-runtime:0.3
        args: [
          "-p", "8080",
          "-a", "127.0.0.1:8081",
          "-s", "[YOUR PROJECT ID].appspot.com",
          "-v", "[YOUR API VERSION]",
        ]
        ports:
          - containerPort: 8080
      - name: api
        image: gcr.io/[YOUR PROJECT ID]/endpoints-image:latest
        ports:
          - containerPort: 8081
```

**If you don't care about the contentes of the config file, and just want to quickly run this API, all you need to do is update a few fields, which are explained in greater detail in the next secion: "Getting Google Container Engine Ready".**

###The Config Explained###
This is a fairly standard configuration file for Kubernetes, so if you are familiar with GKE / Kubernetes, there should be no surprises here. In this section, we will go section by section and try to explain what is going on.

```
apiVersion: v1
kind: Service
metadata:
  name: first-endpoint
```
We are calling our service first-endpoint

```
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  selector:
    app: first-endpoint
  type: LoadBalancer
```
We are serving our API on port 80, using TCP. We will be applying this port configuration to all the sections labeled with 'app: first-endpoint'

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: first-endpoint
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: first-endpoint
```
Here we see that we are applying our previously discussed port setting to our Kubernetes deployment (which we are also calling first-endpoint). We only need one pod replica for this hello world example.

```
    spec:
      containers:
      - name: esp
        image: b.gcr.io/endpoints/endpoints-runtime:0.3
        args: [
          "-p", "8080",
          "-a", "127.0.0.1:8081",
          "-s", "[YOUR PROJECT ID].appspot.com",
          "-v", "[YOUR API VERSION]",
        ]
        ports:
          - containerPort: 8080
```



##Getting Google Container Engine Ready
Ok, so with our simple backend build, and our API spec'd out with Swagger, let's deploy it to GKE and manage it with Google Cloud Endpoints.

As this is where we start working 'in the cloud', a quick reminder on the prerequisites:

1. You have created a Google Cloud Platform project, it has billing enabled, and you know the project ID.
2. You have installed the Cloud SDK.
3. You have installed Docker.

Ensure you are autheticated into the Cloud SDK, and you have set the SDK config to point to the correct project

```
gcloud auth login
```

```
gcloud config set project [YOUR PROJECT ID]
```

Create your cluster, this is where we will be deploying our API, and the Endpoints Server Proxy to manage our API:
```
gcloud container clusters create api-cluster
```

Build your docker image from the Dockerfile attached. This will configure the container such that it can run our API backend successfully:

```
docker build -f /path/to/your/Dockerfile .
```

Tag your newly created image. This is really a readability thing, for ease of identification of the image we just built. First list images to get your id, then tag it:

```
docker images
```
```
docker tag [YOUR IMAGE ID] gcr.io/[YOUR PROJECT ID]/endpoints-image
```

And now push the image to Google Container Registry:

```
gcloud docker push gcr.io/[YOUR PROJECT ID]/endpoints-image
```

##Deploying Your API

First, we need to let the Google service manager know about our API. This doesn't deploy our backend, but allows Google Cloud Endpoints to know how our API is designed, allowing us to make use of all its API management functionality.

Please note, this command is currently in Beta, so if you haven't already, you will need to install the beta components for gcloud (when you run the command, you will be kicked into the download flow automatically, if you need to).

```
gcloud beta service-management deploy swagger.yaml
```

There will be a bit of output from this command, but the most important thing to note is this line:

```
Service Configuration with version [VERSION] uploaded for service [YOUR PROJECT ID.appspot.com]
```

You will need the version and the service (although you should already know the service, you set it in your swagger.yaml) later when configuring your GKE cluster.

Open the my_first_endpoints_GKE.yaml file, and update the service and version fields with the values returned from the prior command. 

```
containers:
      - name: esp
        image: b.gcr.io/endpoints/endpoints-runtime:0.3
        args: [
          "-p", "8080",
          "-a", "127.0.0.1:8081",
          "-s", "[YOUR PROJECT ID].appspot.com",
          "-v", "[VERSION]",
        ]
```

To be clear, don't include the square brackets [ ], your service (-s) and version (-v) should look something like myproject.appspot.com and 2016-10-23r0

Let's now deploy our API backend to GKE, along with the Endpoints Server proxy.

First, we need to authenticate kubectl to the cluster we previously created:

```
gcloud container clusters get-credentials api-cluster
```

Then we deploy our API:

```
kubectl create -f my_first_endpoints_GKE.yaml
```

And now get the external IP, BECAUSE WE ARE NEARlY READY TO CALL OUR API

```
kubectl get service
```


##Testing Your API

##Viewing the Endpoints GUI

##Next Episode

That's it for Part One. To recap, we built a simple API backend, using Python + Flask. We created a Docker container image to successfully run our API backend. We spec'd out our API using the OpenAPI (swagger) spec. We set up Google Container Engine to serve our API. We deployed our API, along with the Endpoints Server Proxy to GKE. We tested our API and saw that it was serving traffic. We viewed the usage graphs and logs for our API in the Google Cloud Console.

But, what next?

Properly versioning an API is critical. You don't want to break your clients. In Part Two, we discuss API versioning, tweak our API, and deploy a new version.

In Part Three, we will then protect access to our API using API keys. 

Until next time!
