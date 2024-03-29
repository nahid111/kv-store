FROM python:3.11.5-alpine

ENV INSTALL_PATH /code
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY ./requirements.txt $INSTALL_PATH
RUN pip install --no-cache-dir --requirement $INSTALL_PATH/requirements.txt

COPY . $INSTALL_PATH

CMD ["python3", "app.py"]