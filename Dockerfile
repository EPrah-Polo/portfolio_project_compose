# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:slim

#EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ADD . /code

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /code

COPY ./data/server/nucamp_server.json /home/pgadmin/

USER root
RUN chown pgadmin:pgadmin /home/pgadmin/nucamp_server_backup.json
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