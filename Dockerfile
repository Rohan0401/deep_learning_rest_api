FROM python:3.5.4
LABEL maintainer="Rohan Rajput, rohan.rajput4@gmail.com"

RUN apt-get update -y
RUN apt-get install -y build-essential
RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
