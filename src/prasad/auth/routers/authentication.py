from fastapi import APIRouter, HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.prasad.auth.model.user import UserModel
from src.prasad.auth.schemas.otp_verify import UserOTPVerify
from src.prasad.auth.schemas.user import UserCreate
from src.prasad.utils.get_hashed_password import get_hashed_password,verify_password
from src.prasad.utils.otp_generate import generate_otp
from src.prasad.utils.email_config import send_otp, SendOtpModel
from src.prasad.utils.token_generation import create_access_token
from src.prasad.utils.user_role import UserRole
from src.prasad.utils.otp_status import OTPStatus
from src.prasad.utils.account_status import AccountStatus



router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)



@router.post("/customer/signup",status_code=status.HTTP_201_CREATED)
async def register_user_customer(user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = await UserModel.find_one(UserModel.email == user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    otp=generate_otp()
    new_user = UserModel(
        email=user.email,
        password=hashed_password,
        account_status=AccountStatus.NOT_VERIFIED,
        role=UserRole.CUSTOMER,
        otp_status=OTPStatus.NOT_VERIFIED,
        otp=otp
    )
    await new_user.insert()
    send_otp_data = SendOtpModel(email=new_user.email, otp=new_user.otp)
    await send_otp(send_otp_data)
    return {
        "message": "User registered successfully.Please check your email.A 6 digit otp has been sent.",
        "data":new_user,
        "otp": new_user.otp
    }


@router.post("/operator/signup",status_code=status.HTTP_201_CREATED)
async def register_user_operator(user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = await UserModel.find_one(UserModel.email == user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    otp=generate_otp()
    new_user = UserModel(
        email=user.email,
        password=hashed_password,
        account_status=AccountStatus.NOT_VERIFIED,
        role=UserRole.OPERATOR,
        otp_status=OTPStatus.NOT_VERIFIED,
        otp=otp
    )
    await new_user.insert()
    send_otp_data = SendOtpModel(email=new_user.email, otp=new_user.otp)
    await send_otp(send_otp_data)
    return {
        "message": "User registered successfully.Please check your email.A 6 digit otp has been sent.",
        "data":new_user,
        "otp": new_user.otp
    }




@router.post("/admin/signup",status_code=status.HTTP_201_CREATED)
async def register_user_admin(user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = await UserModel.find_one(UserModel.email == user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    otp=generate_otp()
    new_user = UserModel(
        email=user.email,
        password=hashed_password,
        account_status=AccountStatus.NOT_VERIFIED,
        role=UserRole.ADMIN,
        otp_status=OTPStatus.NOT_VERIFIED,
        otp=otp
    )
    await new_user.insert()
    send_otp_data = SendOtpModel(email=new_user.email, otp=new_user.otp)
    await send_otp(send_otp_data)
    return {
        "message": "User registered successfully.Please check your email.A 6 digit otp has been sent.",
        "data":new_user,
        "otp": new_user.otp
    }






@router.post("/field_agent/signup",status_code=status.HTTP_201_CREATED)
async def register_user_field_agent(user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = await UserModel.find_one(UserModel.email == user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    otp=generate_otp()
    new_user = UserModel(
        email=user.email,
        password=hashed_password,
        account_status=AccountStatus.NOT_VERIFIED,
        role=UserRole.CUSTOMER,
        otp_status=OTPStatus.NOT_VERIFIED,
        otp=otp
    )
    await new_user.insert()
    send_otp_data = SendOtpModel(email=new_user.email, otp=new_user.otp)
    await send_otp(send_otp_data)
    return {
        "message": "User registered successfully.Please check your email.A 6 digit otp has been sent.",
        "data":new_user,
        "otp": new_user.otp
    }




@router.post("/marketing/signup",status_code=status.HTTP_201_CREATED)
async def register_user_marketing_operator(user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = await UserModel.find_one(UserModel.email == user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    otp=generate_otp()
    new_user = UserModel(
        email=user.email,
        password=hashed_password,
        account_status=AccountStatus.NOT_VERIFIED,
        role=UserRole.CUSTOMER,
        otp_status=OTPStatus.NOT_VERIFIED,
        otp=otp
    )
    await new_user.insert()
    send_otp_data = SendOtpModel(email=new_user.email, otp=new_user.otp)
    await send_otp(send_otp_data)
    return {
        "message": "User registered successfully.Please check your email.A 6 digit otp has been sent.",
        "data":new_user,
        "otp": new_user.otp
    }




@router.post("/otp-verify", status_code=status.HTTP_200_OK)
async def verify_otp(user:UserOTPVerify):
    db_user =await UserModel.find_one(UserModel.email == user.email)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.otp != db_user.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Wrong OTP")

    db_user.otp_status=OTPStatus.VERIFIED
    await db_user.save()
    return {"message":"You have  verified","data":db_user}








@router.post("/login", status_code=status.HTTP_200_OK)

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await UserModel.find_one(UserModel.email == form_data.username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")

    if not db_user.otp_status == OTPStatus.VERIFIED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account is not verified with otp")

    if not db_user.account_status==AccountStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You account is not active, please wait for admin approval or contact your administrator")

    token = create_access_token(data={"sub": db_user.email, "role": db_user.role.value, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}






@router.post("/resend-otp", status_code=status.HTTP_200_OK)
async def resend_otp(email:str):
    db_user = await UserModel.find_one(UserModel.email == email)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    otp=generate_otp()
    db_user.otp=otp
    await db_user.save()
    send_otp_data = SendOtpModel(email=db_user.email, otp=db_user.otp)
    await send_otp(send_otp_data)
    return {
        "message": "User registered successfully.Please check your email.A 6 digit otp has been sent.",
        "data":db_user,
        "otp":db_user.otp
    }





@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(new_password:str,email:str):
    db_user = await UserModel.find_one(UserModel.email == email)
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    if not db_user.otp_status == OTPStatus.VERIFIED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Your account is not verified with otp")

    hashed_password = get_hashed_password(new_password)
    db_user.password = hashed_password
    await db_user.save()
    return {"message":"successfully reset password"}





