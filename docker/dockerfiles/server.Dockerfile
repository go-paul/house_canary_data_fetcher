FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV USERNAME house_canary_data_fetcher
ENV HOME_PATH /home/${USERNAME}
ENV APP_ROOT ${HOME_PATH}/project

# Install system requirements
RUN apk update
RUN apk add build-base python3-dev musl-dev

# Install pip requirements
ADD requirements.txt /
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Create and change user
RUN adduser ${USERNAME} -h ${HOME_PATH} -s /bin/bash -D
USER ${USERNAME}:${USERNAME}

# Set workdir
RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
