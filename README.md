# dms-storage
Project for storage spage control at Dallas Makerspace

## Libraries Used
- SQLAlchemy - Database ORM
- Alembic - Database schema versioning
- FastAPI - REST API
- Authlib - 
  
## Quickstart
Quickest way to get going is to use the docker compose to bring up a couple of docker containers containing the database and the code. 

docker compose up
    frontend: http://localhost:4200
    restapi: http://localhost:8080
    phpldapadmin: http://localhost:8888
    phpmyadmin: http://localhost:8081

ldap login:  cn=admin,dc=dms,dc=local / Adm1n! 
mysql login:  Not needed.  Otherwise root / example

all user (user1, user2, user3, user4) passwords set to "password


Generate new keys
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
# Don't add passphrase
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
cat jwtRS256.key
cat jwtRS256.key.pub


# Architechture
backend - database (Postgresql) backend and API
frontend - React UI
kiosk - Raspberry Pi based UI and backend designed to act as a kiosk with receipt printer and RFID reader

# UI / Endpoint functionality TODO
- auth/Login
- storage/Allocate new Storage
- storage/allocate new w/ quiz
- storage/View Current storages
- storage/View Past Storage 
- Admin View
- View all current storage
- View all storage of user
- View all previous storage
- View all expired storage
- Mark storage to close
- Close storage
- Ban user
- Unban user
- kiosk/badge-in
- kiosk/storage
- 

# Notes
Build using cookiecutter and [Buuntu/fastapi-react](https://github.com/Buuntu/fastapi-react)
