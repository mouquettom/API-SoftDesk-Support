from django.conf import settings
from django.db import models


class Project(models.Model):
    """ Projet """

    # Types autorisés pour un projet
    TYPE_BACKEND = 'back-end'
    TYPE_FRONTEND = 'front-end'
    TYPE_IOS = 'iOS'
    TYPE_ANDROID = 'Android'

    # Choix disponibles pour le champ 'type'
    TYPE_CHOICES = [
        (TYPE_BACKEND, 'back-end'),
        (TYPE_FRONTEND, 'front-end'),
        (TYPE_IOS, 'iOS'),
        (TYPE_ANDROID, 'Android')
    ]


    title = models.CharField(max_length=128)  # Nom du projet
    description = models.TextField()  # Description du projet
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)  # back-end, front-end, iOS, Android

    # Auteur du projet : utilisateur qui l'a créé
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Date de création auto
    updated_at = models.DateTimeField(auto_now=True)  # Date de modification auto

    def __str__(self) -> str:
        return f"Project #{self.title} ({self.author.username})"


class Contributor(models.Model):
    """ Lien : utilisateur / projet """

    # Utilisateur contributeur
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributors',
    )

    # Projet auquel l'utilisateur contribue
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='contributors',
    )

    # Date d'ajout du contributeur
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Empêche d'ajouter deux fois le même utilisateur au même projet
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_user_project')
        ]

    def __str__(self):
        return f"Contributor : {self.user.username} -> Project #{self.project.title}"