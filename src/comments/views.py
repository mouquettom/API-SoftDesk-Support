from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from issues.models import Issue
from .serializers import CommentSerializer
from projects.permissions import IsContributor, IsAuthorOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet complet pour les commentaires

    ModelViewSet fournit automatiquement :
    - list
    - create
    - retrieve
    - update
    - partial_update
    - destroy
    """

    serializer_class = CommentSerializer

    # L'utilisateur doit :
    # - être authentifié
    # - être contributeur du projet
    # - être auteur du commentaire pour modifier/supprimer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retourne uniquement les commentaires de l'issue ciblée,
        en vérifiant aussi que cette issue appartient bien au projet ciblé

        Exemple :
        /api/projects/3/issues/8/comments/
        → retourne les commentaires de l'issue 8 du projet 3
        """
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['issue_pk']

        return Comment.objects.filter(
            issue_id=issue_id,
            issue__project_id=project_id,
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Personnalise la création d'un commentaire

        Le client n'envoie pas author ni issue dans le body :
        - author = utilisateur connecté
        - issue_id = issue récupérée depuis l'URL
        """
        project_id = self.kwargs['project_pk']
        issue_id = self.kwargs['issue_pk']

        # Sécurité supplémentaire :
        # on vérifie que l'issue indiquée dans l'URL appartient bien au projet indiqué
        if not Issue.objects.filter(id=issue_id, project_id=project_id).exists():
            raise NotFound("Cette tâche ne concerne pas ce projet")

        serializer.save(author=self.request.user, issue_id=issue_id)