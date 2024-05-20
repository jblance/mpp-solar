FROM python:slim

# RUN pip install mppsolar
COPY . /mpp-solar/
RUN pip install /mpp-solar/