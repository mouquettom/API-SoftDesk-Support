from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from issues.models import Issue
from issues.serializers import IssueSerializer
from projects.permissions import IsContributor, IsAuthorOrReadOnly


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet complet pour les issues

    ModelViewSet fournit automatiquement :
    - list
    - create
    - retrieve
    - update
    - partial_update
    - destroy
    """

    serializer_class = IssueSerializer

    # L'utilisateur doit :
    # - être authentifié
    # - être contributeur du projet
    # - être auteur pour modifier/supprimer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retourne uniquement les issues du projet ciblé dans l'URL

        Exemple :  /api/projects/3/issues/  → retourne les issues du projet 3
        """
        project_id = self.kwargs['project_pk']
        # Visible uniquement si l'utilisateur courant est aussi contributeur
        return Issue.objects.filter(project_id=project_id).order_by('-created_at')

    def get_serializer_context(self):
        """
        Ajoute project_id au contexte du serializer

        Cela permet au serializer de vérifier que l'assignee
        est bien contributeur du projet courant.
        """
        ctx = super().get_serializer_context()
        ctx['project_id'] = self.kwargs.get('project_pk')
        return ctx

    def perform_create(self, serializer):
        """
        Personnalise la création d'une issue

        Le client n'envoie pas author ni project dans le body :
        - author = utilisateur connecté
        - project_id = projet récupéré depuis l'URL
        """
        project_id = self.kwargs['project_pk']
        serializer.save(author=self.request.user, project_id=project_id)