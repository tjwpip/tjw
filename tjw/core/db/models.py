from datetime import datetime
from typing import Optional


class OperationLog:
    def __init__(self, id: int = None, operation_type: str = None, module: str = None,
                 details: str = None, ip_address: str = None, created_at: datetime = None):
        self.id = id
        self.operation_type = operation_type
        self.module = module
        self.details = details
        self.ip_address = ip_address
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'operation_type': self.operation_type,
            'module': self.module,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SFZRecord:
    def __init__(self, id: int = None, id_number: str = None, region: str = None,
                 birth_date: str = None, gender: str = None, operation: str = None,
                 created_at: datetime = None):
        self.id = id
        self.id_number = id_number
        self.region = region
        self.birth_date = birth_date
        self.gender = gender
        self.operation = operation
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'id_number': self.id_number,
            'region': self.region,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'operation': self.operation,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserSetting:
    def __init__(self, id: int = None, key: str = None, value: str = None,
                 description: str = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.key = key
        self.value = value
        self.description = description
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class User:
    def __init__(self, id: int = None, username: str = None, password_hash: str = None,
                 email: str = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }