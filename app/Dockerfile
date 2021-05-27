FROM python:3.9.5-slim-buster
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development 
ENV DATABASE_URL="mysql+mysqlconnector://root:example@db:3306/dms-storage"
#RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "./bin/wait-for-it.sh", "db:3306", "-s", "--", "./bin/start.sh" ]