from sqlalchemy.orm import Session

from models.user import User
from security import verify_password
from jwt_manager import create_access_token


class AuthService:

    @staticmethod
    def create_user(
        db: Session,
        nom: str,
        prenom: str,
        email: str,
        password: str,
        role: str = "USER"
    ):

        user = User(
            nom=nom,
            prenom=prenom,
            email=email,
            password_hash=password,
            role=role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ):

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash
        ):
            return None

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role
            }
        )

        return token