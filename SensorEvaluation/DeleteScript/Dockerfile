# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY ./requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./src/ .

ARG ARG_DB_HOST
ARG ARG_DB_PORT
ARG ARG_DB_NAME
ARG ARG_DB_USER
ARG ARG_DB_PASSWD

ENV DB_HOST "$ARG_DB_HOST"
ENV DB_PORT "$ARG_DB_PORT"
ENV DB_NAME "$ARG_DB_NAME"
ENV DB_USER "$ARG_DB_USER"
ENV DB_PASSWD "$ARG_DB_PASSWD"


# command to run on container start
ENTRYPOINT [ "python", "./delete_script" ]