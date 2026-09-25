FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y vnc4server jwm firefox

ADD startup_script.sh /startup_script.sh
RUN chmod +x /startup_script.sh

ADD mypass /mypass

# Update the image
RUN echo "random238998355" # Change to break cache and cause update/upgrade
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install firefox

#Set environment variables
ENV DISPLAY :0

CMD ./startup_script.sh
