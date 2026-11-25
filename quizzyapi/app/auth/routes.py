from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.users.model import User
from app.profiles.model import Profile
from app.auth.schemas import SignUpRequest, SignInRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth",tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignUpRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail already exists!"
        )
        
    if data.password != data.confirmed_password:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="As senhas não coincidem"
      )

    hashed_password = hash_password(data.password)

    new_user = User(
        email=data.email,
        hashed_password=hashed_password,
        is_active=True,
    )

    new_user.profile = Profile(
        full_name=data.full_name
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )

    return {
        "id": str(new_user.id),
        "email": new_user.email,
        "full_name": new_user.profile.full_name,
        "message": "Conta criada com sucesso"
    }

@router.post("/signin", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def signin(data: SignInRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail or Password are incorrects"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada"
        )

    access_token = create_access_token(
        user_id=str(user.id)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }