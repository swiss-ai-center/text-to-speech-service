# Base image
FROM python:3.11

# Install all required packages to run the model
# TODO: 1. Add any additional packages required to run your model
# RUN apt update && apt install --yes package1 package2 ...
# Install dependencies

# Copy requirements file
COPY ./requirements.txt .
COPY ./requirements-all.txt .

RUN apt update
RUN apt install -y ffmpeg libavcodec-extra
RUN pip install --requirement requirements.txt --requirement requirements-all.txt