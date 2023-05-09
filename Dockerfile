FROM python:3.9-buster

RUN pip install mppsolar
ENTRYPOINT ["mpp-solar"]
CMD ["--help"]
