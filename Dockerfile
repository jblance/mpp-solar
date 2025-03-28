FROM python:3.12

RUN pip install --upgrade pip
RUN python -V
RUN python -c 'import platform;print(platform.machine())'
ARG TARGETARCH
RUN echo $TARGETARCH
# RUN if [ "$TARGETARCH" = "arm64" ] ; then \
#         pip install https://github.com/mosquito/cysystemd/releases/download/1.6.2/cysystemd-1.6.2-cp312-cp312-manylinux_2_28_aarch64.whl ; \
#     elif [ "$TARGETARCH" = "arm" ] ; then \
#         pip install https://github.com/mosquito/cysystemd/releases/download/1.6.2/cysystemd-1.6.2-cp312-cp312-manylinux_2_28_aarch64.whl ; \
#     else \
#         pip install https://github.com/mosquito/cysystemd/releases/download/1.6.2/cysystemd-1.6.2-cp312-cp312-manylinux_2_28_x86_64.whl ; \
#     fi
COPY . /mpp-solar/
RUN pip install /mpp-solar/
