# Install the latest alpine linux which is docker default
FROM alpine:latest
# install python3 and pip in container 
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip


# set the working directory to /app
WORKDIR /app

# copy the content of current folder to the /app folder of the image
COPY . /app

# run the command pip3 to  install requiremenrs on the image
RUN pip3 install -r requirements.txt
RUN python3 -m textblob.download_corpora

# expose the port 5000 
EXPOSE 5000

# entry point is the command node when container starts
ENTRYPOINT ["python3"]

# the arguments of entry command : i.e command is : python3 app.py
CMD ["app.py"]