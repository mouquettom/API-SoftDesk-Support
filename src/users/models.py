from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def validate_age(value):
    """ Valide l'âge de l'utilisateur """
    if value < 15:
        raise ValidationError("L'utilisateur doit au minimum avoir 15 ans lors de l'inscription.")


class User(AbstractUser):
    """
    Modèle utilisateur personnalisée

    Il hérite de AbstractUser, donc il conserve les champs Django standards :
    -> username, password, email, first_name, last_name, is_staff, etc
    """

    # Âge obligatoire, validé avec validate_age
    # validators=[validate_age] : Django appliquera la fonction validate_age() pour vérifier la valeur
    age = models.PositiveSmallIntegerField(validators=[validate_age])

    # Consentement : l'utilisateur accepte-t-il d'être contacté ?
    can_be_contacted = models.BooleanField(default=False)

    # Consentement : l'utilisateur accepte-t-il le partage de ses données ?
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username