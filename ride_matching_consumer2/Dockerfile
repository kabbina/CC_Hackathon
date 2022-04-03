# Dockerfile for ride matching consumer


FROM python:3.7
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=1

WORKDIR /ride_matching_consumer2

COPY . /ride_matching_consumer2/


ENTRYPOINT [ "python3" ]

CMD [ "ride_matching_consumer2.py" ]
