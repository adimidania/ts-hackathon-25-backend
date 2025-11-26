from pydantic import BaseModel


class GenerateStoryRequest(BaseModel):
    prompt_vars: dict | None = None

class GenerateImageRequest(BaseModel):
    prompt: str

class GenerateStoryResponse(BaseModel):
    text: str

class GenerateImageResponse(BaseModel):
    image_url: str

class GenerateAudioRequest(BaseModel):
    prompt: str

class LoginParentRequest(BaseModel):
    email: str
    password: str
class RegisterParentRequest(BaseModel):
    email: str
    full_name: str
    phone_number: str
    password: str