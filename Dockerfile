FROM ubuntu:latest
MAINTAINER Your Name "your@name.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE  8081
ENTRYPOINT ["python"]
CMD ["my_first_endpoint.py"]