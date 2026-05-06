from django.conf import settings
from django.db import models

from projects.models import Project


class Issue(models.Model):
    """ Tâche ou Problème -> lié à un Projet """

    # Priorités possibles
    PRIORITY_LOW = 'LOW'
    PRIORITY_MEDIUM = 'MEDIUM'
    PRIORITY_HIGH = 'HIGH'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'LOW'),
        (PRIORITY_MEDIUM, 'MEDIUM'),
        (PRIORITY_HIGH, 'HIGH'),
    ]

    # Types possibles d'issue
    TAG_BUG = 'BUG'
    TAG_FEATURE = 'FEATURE'
    TAG_TASK = 'TASK'

    TAG_CHOICES = [
        (TAG_BUG, 'BUG'),
        (TAG_FEATURE, 'FEATURE'),
        (TAG_TASK, 'TASK'),
    ]

    # Statuts possibles
    STATUS_TODO = 'To Do'
    STATUS_INPROGRESS = 'In Progress'
    STATUS_FINISHED = 'Finished'

    STATUS_CHOICES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_INPROGRESS, 'In Progress'),
        (STATUS_FINISHED, 'Finished'),
    ]

    title = models.CharField(max_length=128)  # Titre de l'issue
    description = models.TextField()  # Description détaillée de l'issue

    priority = models.CharField(max_length=32, choices=PRIORITY_CHOICES)  # Priorité : LOW, MEDIUM ou HIGH
    tag = models.CharField(max_length=32, choices=TAG_CHOICES)  # Nature de l'issue : BUG, FEATURE ou TASK
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_TODO)  # Statut

    # Projet auquel l'issue appartient
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues',
    )

    # Auteur de l'issue : utilisateur qui l'a créée
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='issues_author',
    )

    # Utilisateur assigné à l'issue (facultatif) : une issue peut exister sans assigné
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='issues_assignee',
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Date de création auto
    updated_at = models.DateTimeField(auto_now=True)  # Date de dernière modification auto

    def __str__(self) -> str:
        return f"Issue #{self.title} -> Project #{self.project.title}"