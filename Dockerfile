FROM python:3.12

RUN pip install --upgrade pip
RUN python -V
RUN python -c 'import platform;print(platform.machine())'
RUN pip install https://github.com/mosquito/cysystemd/releases/download/1.6.2/cysystemd-1.6.2-cp312-cp312-manylinux_2_28_x86_64.whl
COPY . /mpp-solar/
RUN pip install /mpp-solar/
