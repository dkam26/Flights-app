FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /flight_app
WORKDIR /flight_app
COPY requirements.txt /flight_app/
RUN pip install -r requirements.txt
COPY . /flight_app/