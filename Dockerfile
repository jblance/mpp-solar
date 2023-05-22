FROM python:3.10-buster
COPY ./mpp-solar /mpp-solar/
RUN pip install -e /mpp-solar/
