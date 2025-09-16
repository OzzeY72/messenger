from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import hash_password, verify_password, create_access_token
from app.users.repository import UserRepository
from app.users.service import UserService
from app.auth.providers.oauth_factory import get_oauth_provider
from . import schemas

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.user_service = UserService(db)

    async def register_email(self, data: schemas.RegisterEmail):
        hashed_pw = hash_password(data.password)
        print(hashed_pw)
        return await self.user_service.create_user(
            email=data.email,
            name=data.name,
            auth_provider="email",
            hashed_password=hashed_pw,
        )
    
    async def login_email(self, data: schemas.LoginEmail):
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    
    async def login_oauth(self, data: schemas.LoginOAuth):
        provider = get_oauth_provider(data.auth_provider)
        user_info = await provider.get_user_info(data.provider_id)

        user = await self.repo.get_by_email(user_info.get("email"))
        if not user:
            user = await self.user_service.create_user(
                email=user_info.get("email"),
                name=user_info.get("name"),
                auth_provider=data.auth_provider,
            )
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}

    

    