FROM python:3.9.5-slim-buster
WORKDIR /usr/src/app
ENV DATABASE_URL="mysql+mysqlconnector://user:password@db:3306/dms-storage"
#RUN apt-get update
COPY . .
RUN pip install -r requirements.txt
#ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "/usr/src/app/bin/wait-for-it.sh", "db:3306", "-s", "-t", "120", "--", "/usr/src/app/bin/start.sh" ]