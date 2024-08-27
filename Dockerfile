FROM python:slim-bullseye

LABEL maintaner="azita taahbaz"

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/



CMD [ "python","manage.py","runserver","0.0.0.0:8000" ]
