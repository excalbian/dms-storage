# dms-storage
Project for storage control at Dallas Makerspace

## Libraries Used
- SQLAlchemy - Database ORM
- Alembic - Database schema versioning
- FastAPI - REST API
- Authlib - OAuth2 integration (google)
  
## Quickstart
Quickest way to get going is to use the docker compose to bring up a couple of docker containers containing the database and the code. 



Generate new keys
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
# Don't add passphrase
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
cat jwtRS256.key
cat jwtRS256.key.pub


# UI / Endpoing functionality TODO
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