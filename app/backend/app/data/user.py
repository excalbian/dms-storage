from typing import List

from sqlalchemy.orm.session import sessionmaker
from .dbmodels import DbUser, User

class UserAccess():
    def __init__(self, sm:sessionmaker):
        self._session = sm
    
    def get_users(self, skip: int = 0, limit: int = 5000) -> List[User]:
        with self._session() as db:
            users:List[DbUser] = db.query(DbUser) \
                .order_by(DbUser.username) \
                .offset(skip) \
                .limit(limit) \
                .all()
        
            return [ User.from_orm(u) for u in users ]
        

    def get_user_by_username(self, username: str) -> User:
        with self._session() as db:
            dbuser = db.query(DbUser) \
                .filter(DbUser.username == username) \
                .first()
            return None if dbuser is None else User.from_orm(dbuser)
    
    def create_user(self, obj: User) -> User:
        with self._session() as db:
            u = DbUser(
                username = obj.username,
                displayname = obj.displayname,
                email = obj.email,
                phone = obj.phone,
                next_use = obj.next_use
            )
            
            db.add(u)
            db.commit()
            db.refresh(u)
            return User.from_orm(u)
    
    def update_user(self, obj: User) -> User:
        with self._session() as db:
            u = db.query(DbUser).filter(DbUser.id == obj.id) \
            .update(
            {
                DbUser.email: obj.email,
                DbUser.displayname: obj.displayname,
                DbUser.phone: obj.phone,
                DbUser.next_use: obj.next_use,
                DbUser.is_active: obj.is_active,
                DbUser.is_banned: obj.is_banned,
                DbUser.is_admin: obj.is_admin,
                DbUser.can_report: obj.can_report,
                DbUser.can_configure: obj.can_configure,
                DbUser.can_ban: obj.can_ban  
            })
            if u <= 0:
                raise KeyError("User with id {obj.id} not found")
            db.commit()
            updated = db.query(DbUser).get(obj.id)
            return User.from_orm(updated)
    
    def get_user_by_id(self, user_id: int):
        with self._session() as db:
            dbuser = db.query(DbUser).get(user_id)
            return None if dbuser is None else User.from_orm(dbuser)
