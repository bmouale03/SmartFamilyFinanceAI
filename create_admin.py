from database import SessionLocal

from models.user import User

from security import hash_password

db = SessionLocal()

admin = (
    db.query(User)
    .filter(
        User.email ==
        "admin@smartfamily.com"
    )
    .first()
)

if admin is None:

    admin = User(

        nom="Administrateur",

        prenom="Système",

        email=
        "admin@smartfamily.com",

        password_hash=
        hash_password(
            "Admin@2026"
        ),

        role="ADMIN"
    )

    db.add(admin)

    db.commit()

    print(
        "Administrateur créé."
    )

else:

    print(
        "Administrateur existe déjà."
    )