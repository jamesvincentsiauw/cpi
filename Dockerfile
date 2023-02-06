FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install --upgrade certifi
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "-u" , "thread.py"]