from beanie import Document
from pydantic import EmailStr, Field
import uuid
from datetime import datetime, timezone
from prasad.utils.user_role import UserRole
from prasad.utils.account_status import AccountStatus
from prasad.utils.otp_status import OTPStatus

class UserModel(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    email: EmailStr
    password: str
    account_status: AccountStatus
    role: UserRole
    otp_status: OTPStatus
    otp: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    model_config = {
        "collection": "user",
        "from_attributes": True
    }
