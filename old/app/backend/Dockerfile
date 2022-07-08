FROM python:3.9.5-slim-buster
WORKDIR /usr/src/app
ENV DATABASE_URL="mysql+mysqlconnector://user:password@db:3306/dms-storage"
#RUN apt-get update
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt
COPY ./bin /usr/src/appbin
#ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "/usr/src/appbin/wait-for-it.sh", "db:3306", "-s", "-t", "120", "--", "/usr/src/appbin/start.sh" ]