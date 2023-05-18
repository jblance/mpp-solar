FROM python:3.9-buster

RUN pip install mppsolar
COPY powermon/config/*.yaml .
ENTRYPOINT ["powermon"]
CMD ["--help"]
