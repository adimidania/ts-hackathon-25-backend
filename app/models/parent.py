from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Parent(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: str
    hashed_password: str
    stories: List[str] = []
    drafts: List[str] = []
