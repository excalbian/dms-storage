from app.data.user import User
from typing import Optional

class Token(User):
    iss: Optional[int] = None
    sub: Optional[int] = None
