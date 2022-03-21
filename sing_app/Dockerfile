# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.2-slim
# RUN whoami
#https://pythonspeed.com/articles/activate-virtualenv-dockerfile/

#EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV FLASK_APP entry.py
ENV FLASK_ENV production
#https://docs.docker.com/samples/django/ example of dockerfile
WORKDIR /code

COPY . /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN python ./setup.py --load-servers ./data/server/nucamp_server.json

#COPY ./sing_app/data/server/nucamp_server.json /pgadmin4/servers.json
#COPY ./sing_app/data/server/nucamp_server.json /docker-entrypoint-initdb.d/
#RUN chown pgadmin4:pgadmin4 /home/pgadmin4/nucamp_server.json
# RUN useradd -ms /bin/bash <user>
#RUN chmod 777 /pgadmin4/server/nucamp_servers.json

#ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

#CMD ["python", "/code/app/app.py"]
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
