#Download Python from DockerHub and use it
FROM python:3.7.4


#Set the working directory in the Docker container
WORKDIR /code
COPY . /code


#Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ENV FLASK_APP="entry.py"
ENV FLASK_DEBUG="1"
ENV FLASK_ENV="development"

# EXPOSE 5000

#Run the container
CMD [ "flask", "run" ]
