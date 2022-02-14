# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.2-slim
# RUN whoami
#https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# ENV VIRTUAL_ENV=/opt/venv
# RUN python -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV PYTHONPATH "${PYTHONPATH}:/code"

#RUN python -m venv /opt/venv
#https://jonathanmeier.io/using-pipenv-with-docker/
#RUN pip install pipenv

#EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Create app directory
#RUN mkdir -p /code
#ADD . /code

#https://docs.docker.com/samples/django/ example of dockerfile
WORKDIR /code
#ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.10.2/site-packages/"
# Install pip requirements
# install dependencies
#RUN python -m ensurepip --default-pip
#ENV PATH="/code/venv/Scripts:$PATH"
#RUN pip install --upgrade pip
COPY . /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
#RUN pipenv install --deploy --ignore-pipfile
#CMD ["pipenv", "run", "python", "app.py"]
# COPY app/app.py .
# CMD . /opt/venv/bin/activate && exec python /code/app/app.py

CMD ["python", "/code/app/app.py"]
#ENTRYPOINT [ "python", "/code/app/app.py" ] 
#RUN pip install -r requirements.txt
#ENTRYPOINT [ "python", "/code/app/app.py" ] 
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

#---------------MADE PGADMIN WORK---------#
#COPY ./data/server/nucamp_server.json /home/pgadmin/

#USER root
#RUN chown pgadmin4:pgadmin4 /pgadmin4/servers.json

#USER pgadmin4

#COPY . /usr/src/app/
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app\app:app"]
#ENTRYPOINT [ "python", "./app/app.py" ] 

#==================TESTING====================
# FROM python:3.6-slim-buster

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 5000

# CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]