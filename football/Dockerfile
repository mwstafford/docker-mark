FROM ubuntu:latest
MAINTAINER Mark Stafford "mstafford@connextron.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install boto3
#RUN pip install -r requirements.txt
RUN pip install flask
ENTRYPOINT ["python"]
CMD ["app.py"]
