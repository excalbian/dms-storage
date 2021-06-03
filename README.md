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

