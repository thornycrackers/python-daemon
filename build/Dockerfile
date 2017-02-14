FROM ubuntu:16.04
MAINTAINER Cody Hiar <codyfh@gmail.com>

# Set a term for terminal inside the container, can't clear without it
ENV TERM xterm-256color

# Update and install
RUN apt-get update && apt-get install -y \
      htop \
      python3-dev \
      python3-pip

# # Add the project requirements
# ADD requirements.txt /opt/requirements.txt

# The code should be symlinked to this directory
WORKDIR /app

# Create the entry script
ADD entry.sh /opt/
RUN chmod 755 /opt/entry.sh
