FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

ADD . /kv-store
WORKDIR /kv-store

RUN pip install -r requirements.txt

#CMD [ "python3", "./app.py" ]


