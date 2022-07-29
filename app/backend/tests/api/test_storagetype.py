import json
import pytest
from app.main import app

from app.data.storage_type import StorageType, StorageTypeAccess
from app.data.user import User
from app.api import deps

def test_get_storagetype(test_app, monkeypatch):
    test_response_payload = [{"id": 1, "name":"test", "location":"NWFlex","enabled":True,"valid_days":None  }]

    def mock_storagetype(s):
        return [
            StorageType( 
                id = 1,
                name = "test",
                location = "NWFlex",
                enabled = True
            )
        ]
    
    def mock_user():
        return User( id = 1, username="", email="")
    
    monkeypatch.setattr(StorageTypeAccess, "get_enabled", mock_storagetype)
   
    test_app.app.dependency_overrides[deps.get_current_user] = mock_user
    response = test_app.get("/api/v1/storagetype")
    
    assert response.status_code == 200
    assert response.json() == test_response_payload

def test_get_storagetype_loginreq(test_app, monkeypatch):
    test_app.app.dependency_overrides = {}
    response = test_app.get("/api/v1/storagetype")
    
    assert response.status_code == 401