from pydantic import BaseModel
from typing import List, Optional

class Story(BaseModel):
    title: str
    main_character: Optional[str] = None
    age: Optional[int] = None
    characters: Optional[List[str]] = []
    gender: Optional[str]= None
    picture: Optional[str] = None
    paragraph: str
    pictures: Optional[List[str]] = []
    audio: Optional[str] = None
    values: Optional[List[str]]
    style: Optional[str]
    theme: Optional[str]
    islamic_teaching: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    is_draft: bool = False
