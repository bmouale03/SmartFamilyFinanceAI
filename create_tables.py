from database import Base
from database import engine

from models.user import User
from models.membre import Membre
from models.revenu import Revenu
from models.depense import Depense
from models.compte import Compte
from models.epargne import Epargne
from models.objectif import Objectif
from models.devise import Devise
from models.prediction import Prediction
from models.utilisateur import *

Base.metadata.create_all(bind=engine)

print(
    "Base SmartFamily créée avec succès."
)