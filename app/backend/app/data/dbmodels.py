from datetime import datetime
from typing import Optional

from . import DbBase
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, JSON, String, Text  
from sqlalchemy.orm import relationship
import enum
from . import PydanticBase
from pydantic import Field
from datetime import datetime
from typing import Optional, List

class DbUser(DbBase):
    """ User DB Model
        While not the authoritative source for login, as we'll use OAuth for that,
        this model storage basic information about those users for use with this
        system.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), index=True, unique=True)
    displayname = Column(String(100))
    phone = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)
    next_use = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    can_report = Column(Boolean, default=False)
    can_configure = Column(Boolean, default=False)
    can_ban = Column(Boolean, default=False)


class User(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    username: str
    displayname: Optional[str] = None
    phone: Optional[str] = None
    email: str
    is_active: bool = True
    is_banned: bool = False
    is_admin: bool = False
    can_report: bool = False
    can_configure: bool = False
    can_ban: bool = False
    next_use: Optional[datetime] = None

class AuditType(str, enum.Enum):
    """ All types of actions logged in the audit table """
    login = 'login'
    slotreserved = 'slotreserved'
    slotreleased = 'slotreleased'
    userupdated = 'userupdated'
    reportrun = 'reportrun'
    slotupdated = 'slotupdated'
    security = 'security'
    info = 'info'

class DbAuditLog(DbBase):
    """ Represents an audit entry in the database. Used for all
        actions that should be auditable """
    __tablename__ = 'auditlog'
    id = Column(Integer, primary_key=True)
    logtime = Column(DateTime, default=datetime.now)
    logtype = Column(Enum(AuditType))
    user_id = Column(Integer, ForeignKey('user.id'))
    message = Column(Text)
    data = Column(JSON)
    user = relationship(DbUser.__name__)


class AuditLog(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    logtime: datetime = Field(allow_mutation=False, default=datetime.min)
    logtype: AuditType = AuditType.info
    message: str = ""
    data: Optional[dict] = None
    user: User


class DbConfiguration(DbBase):
    """ Configuration DB class
        Represents simple key/value configuration entries for the application. Meant
        to be read once and cached.
    """
    id = Column(Integer, primary_key=True)
    key = Column(String(25), index=True, unique=True)
    value = Column(Text)


class DbKiosk(DbBase):
    """ Kiosk DB Model
        Meant to represent an address or machine name of a kiosk, to 
        automatically put it in a kiosk mode. The printer name will
        be used to connect and print out tags when necessary.
    """
    __tablename__ = 'kiosk'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    printer_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Kiosk(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    name: str
    printer_name: Optional[str] = None

class DbStorageType(DbBase):
    """ StorageType DB Model
        Represents a type of storage - e.g. flex area vertical, flex area shelf, 
        warehouse large shelf, ikea tub, etc. Should have a name and a location, but is 
        not a reservable space - that is a storage slot.
    """
    __tablename__ = 'storage_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    location = Column(String(30), nullable=True)
    valid_days = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class StorageType(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    name: str
    location: str
    valid_days: Optional[int]
    enabled: bool = True

class DbStorageSlot(DbBase):
    """ Storage Slot DB Model
        Represents a single reserveable place for storage.
    """
    __tablename__ = 'storage_slot'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    storage_type_id = Column(Integer, ForeignKey(DbStorageType.id))
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    storage_type = relationship(DbStorageType)
    storage = relationship('DbStorage', back_populates='slot')


# CRUD - basic crud, no delete
class StorageSlot(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    name: str
    enabled: bool = True
    storage_type: StorageType
    has_storage: bool = False

class StorageStatus(str, enum.Enum):
    """ All types of statuses """
    pending = 'pending'
    active = 'active'
    expired = 'expired'
    closed = 'closed'

class DbStorage(DbBase):
    """ Storage DB Model
        Represents a reservation of a storage slot. Main transactional table for the application
    """
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    slot_id = Column(Integer, ForeignKey('storage_slot.id'), nullable=False)
    started = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(Enum(StorageStatus), default=StorageStatus.pending,  nullable=False)
    expiring = Column(DateTime, nullable=True, index=True)
    ended = Column(DateTime, nullable=True)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    slot = relationship(DbStorageSlot.__name__, back_populates='storage')
    user = relationship(DbUser.__name__)


class Storage(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    started: Optional[datetime]
    status: Optional[StorageStatus]
    expiring: Optional[datetime]
    ended: Optional[datetime]
    slot: StorageSlot
    user: User




class HookType(str, enum.Enum):
    """ Types of webhooks available """
    slot_reserved = 'slot_reserved'
    slot_expired = 'slot_expired'
    slot_released = 'slot_released'
    slot_dead = 'slot_dead'
    user_banned = 'user_banned'

class DbWebhook(DbBase):
    """ Webhook DB Model
        Stores registered webhooks to fire when actions happen
    """
    id = Column(Integer, primary_key=True)
    hooktype = Column(Enum(HookType), index=True)
    url = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # TODO: Authentication / Key storage

class Webhook(PydanticBase):
    id: int = Field(allow_mutation=False, default=-1)
    hooktype: HookType
    url: str