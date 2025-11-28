
from beanie import Document
from pydantic import  Field
import  uuid
from enum import Enum

class ImageStatus(Enum):
    PROFILE_PICTURE="PROFILE_PICTURE"

class ImageModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    image_url: str


    model_config = {
        "collection": "images",
        "from_attributes": True
    }
