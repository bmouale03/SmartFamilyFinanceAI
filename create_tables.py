from database import Base, engine

# import des modèles
from models.user import User
from models.compte import Compte
from models.depense import Depense

Base.metadata.create_all(bind=engine)

print("Base créée")