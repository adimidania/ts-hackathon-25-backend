from pydantic import BaseModel


class GenerateStoryRequest(BaseModel):
    prompt_vars: dict | None = None

class GenerateImageRequest(BaseModel):
    prompt: str

class GenerateStoryResponse(BaseModel):
    text: str

class GenerateImageResponse(BaseModel):
    image_url: str
