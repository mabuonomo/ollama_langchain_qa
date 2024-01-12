FROM python:3.11-slim

ENV PIP_ROOT_USER_ACTION=ignore

RUN apt update && apt install -y wget make
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)"

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip --version
