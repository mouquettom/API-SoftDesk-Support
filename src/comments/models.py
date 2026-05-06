import uuid

from django.conf import settings
from django.db import models

from issues.models import Issue


class Comment(models.Model):
    """ Commentaire -> lié à un Issue """

    # Identifiant unique UUID demandé par le brief
    # Il remplace l'id numérique classique
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Contenu du commentaire
    description = models.TextField()

    # Issue à laquelle le commentaire est rattaché
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    # Auteur du commentaire
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments_author',
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Date de création auto

    def __str__(self) -> str:
        """ Affiche l'UUID du commentaire """
        return str(self.id)