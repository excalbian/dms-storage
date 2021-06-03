FROM python:3.9.5-slim-buster
WORKDIR /usr/src/app
ENV DATABASE_URL="mysql+mysqlconnector://user:password@db:3306/dms-storage"
#RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "./bin/wait-for-it.sh", "db:3306", "-s", "-t", "120", "--", "./bin/start.sh" ]