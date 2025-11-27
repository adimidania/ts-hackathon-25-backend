from pydantic import BaseModel
from typing import Optional


class ChildInformation(BaseModel):
    name: str
    favorite_pet_name: Optional[str] = None
    friends_names: Optional[list[str]] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None


class GenerateStoryRequest(BaseModel):
    child_information: ChildInformation
    story_goal: str
    tags: Optional[list[str]] = None
    story_length: str
    story_theme: str
    include_islamic_teaching: bool = False
    additional_instructions: Optional[str] = None


class GenerateStoryResponse(BaseModel):
    title: str
    text: str

class NarrationRequest(BaseModel):
    title: str
    text: str

class NarrationResponse(BaseModel):
    title: str
    audio_path: str
