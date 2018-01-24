FROM tensorflow/tensorflow:latest-gpu

ARG USER_NAME
ARG USER_PASSWORD
ARG USER_ID
ARG USER_GID

RUN apt-get update
RUN apt install sudo
RUN useradd -ms /bin/bash $USER_NAME
RUN usermod -aG sudo $USER_NAME
RUN yes $USER_PASSWORD | passwd $USER_NAME

# set uid and gid to match those outside the container
RUN usermod -u $USER_ID $USER_NAME 
RUN groupmod -g $USER_GID $USER_NAME

WORKDIR /home/$USER_NAME


# set the terminator inside the docker container to be a different color
RUN mkdir -p .config/terminator
COPY ./docker/terminator_config .config/terminator/config
RUN chown $USER_NAME:$USER_NAME -R .config


ENTRYPOINT bash -c "/bin/bash"