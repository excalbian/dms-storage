from flask_restful import Api, Resource, request

from .models.auditlog import AuditLog, AuditLogSchema
from .models.configuration import Configuration
from .models.kiosk import Kiosk
from .models.permissions import Permissions
from .models.storage_slot import StorageSlot
from .models.storage_type import StorageType
from .models.user import User, UserSchema
from .models.webhook import Webhook
from .models.storage import Storage, StorageSchema

from .appdef import app
import json

api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


class ApiUser(Resource):
    def get(self, id):
        u = User.query.get(id)
        if u is None:
            return None, 404
        else:
            app.logger.info(u.id)
            return UserSchema().dump(u)

class ApiUsers(Resource):
    def get(self):
        u = User.query.all()
        app.logger.info(len(u))

        return UserSchema(many=True).dump(u)

class ApiHistory(Resource):
    def get(self):
        args = request.args
        user_id = args.get('user_id')
        al = AuditLog.query.filter(AuditLog.user_id == user_id)
        return AuditLogSchema(many=True).dump(al)

class ApiStorage(Resource):
    def get(self):
        args = request.args
        user_id = args.get('user_id')
        s = Storage.query.filter(Storage.user_id == user_id)
        return StorageSchema(many=True).dump(s)
        
api.add_resource( ApiUser, "/api/v0.1/user/<int:id>")
api.add_resource( ApiUsers, "/api/v0.1/users")
api.add_resource( ApiHistory, "/api/v0.1/history" )
api.add_resource( ApiStorage, "/api/v0.1/storage")