from pydantic import BaseModel
from typing import List, Optional

class Story(BaseModel):
    title: str
    main_character: str
    age: int
    characters: List[str]
    gender: str
    picture: Optional[str] = None
    paragraph: str
    pictures: List[str] = []
    audio: Optional[str] = None
    values: List[str]
    style: str
    theme: str
    islamic_teaching: str
    description: str
    tags: List[str]
    is_draft: bool = False
