import pydantic
import requests as requests

from typing import Optional
from errors import HttpError

class BaseUser(pydantic.BaseModel):
    username: str
    password: str

    @pydantic.field_validator('password')
    @classmethod
    def secure_password(cls, v: str):
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        return v

class CreateUser(BaseUser):   #
    username: str
    password: str
    email: Optional[str] = 'missing@email'

class PatchUser(BaseUser):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

class BaseAd(pydantic.BaseModel):
    user_id: int
    header: Optional[str] = None
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    @classmethod
    def validate_ad_owner(cls, value):
        url = f'http://localhost:5000/user/{value}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError('user not found...')
        return value

class CreateAd(BaseAd):
    user_id: int
    header: Optional[str] = 'made ad'
    description: Optional[str] = None

class PatchAd(BaseAd):   # валидация рекламы
    user_id: Optional[int] = None
    header: Optional[str] = None
    description: Optional[str] = None

def validate(schema: type[CreateUser | PatchUser | CreateAd | PatchAd], json_data: dict):
    try:
        schema_instance = schema(**json_data)
        return schema_instance.model_dump(exclude_unset=True)
    except pydantic.ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)
