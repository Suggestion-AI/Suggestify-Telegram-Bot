FROM python:3.11-buster

RUN apt-get update -y && \
    apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

CMD ["python", "./run.py"]
