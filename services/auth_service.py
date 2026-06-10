from sqlalchemy.orm import Session

from models.user import User

from security import (
    hash_password,
    verify_password
)

from jwt_manager import create_access_token


class AuthService:

    @staticmethod
    def create_user(
        db: Session,
        nom: str,
        prenom: str,
        email: str,
        password: str,
        role: str = "Utilisateur"
    ):

        # Vérifier si l'utilisateur existe déjà

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:

            raise ValueError(
                "Cet email est déjà utilisé."
            )

        # Hashage du mot de passe

        password_hash = hash_password(
            password
        )

        # Création de l'utilisateur

        user = User(
            nom=nom,
            prenom=prenom,
            email=email,
            password_hash=password_hash,
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

        # Recherche de l'utilisateur

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:

            return None

        # Vérification du mot de passe

        if not verify_password(
            password,
            user.password_hash
        ):

            return None

        # Génération du JWT

        token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id,
                "role": user.role
            }
        )

        return token

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: int
    ):

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_all_users(
        db: Session
    ):

        return (
            db.query(User)
            .order_by(User.nom)
            .all()
        )

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:

            return False

        db.delete(user)

        db.commit()

        return True

    @staticmethod
    def update_user_role(
        db: Session,
        user_id: int,
        role: str
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:

            return False

        user.role = role

        db.commit()

        return True