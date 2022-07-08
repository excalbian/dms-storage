import json
import pytest
from app.main import app
from datetime import datetime, timedelta
from app.data.storage import Storage
from app.data.user import User
from app.api import deps

def test_get_storage_loginreq(test_app, monkeypatch):
    test_app.app.dependency_overrides = {}
    response = test_app.get("/api/v1/storage/1")
    
    assert response.status_code == 401