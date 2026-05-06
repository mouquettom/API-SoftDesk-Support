from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Project, Contributor


class IsContributor(BasePermission):
    """
    Vérifie que l'utilisateur connecté est contributeur du projet concerné
    """

    def has_permission(self, request, view):
        # Récupère l'id du projet :
        # — project_pk  pour les routes imbriquées
        # — pk  pour les routes classiques  /projects/<pk>/
        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')

        # Si aucun projet précis n'est ciblé, on laisse passer
        # -> le filtrage se fera dans get_queryset()
        if not project_id:
            return True

        # Autorise seulement si l'utilisateur est contributeur du projet
        return Contributor.objects.filter(
            project_id=project_id,
            user=request.user,
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Si l'objet est directement un Projet
        if isinstance(obj, Project):
            project = obj
        else:
            # Sinon, on tente de récupérer le projet depuis l'objet
            # Exemple : une Issue possède obj.project
            project = getattr(obj, 'project', None)

            # Exemple : un Comment possède obj.issue.project
            if project is None and hasattr(obj, 'issue'):
                project = obj.issue.project

        # Vérifie que l'utilisateur est contributeur du projet retrouvé
        return Contributor.objects.filter(
            project=project,
            user=request.user,
        ).exists()


class IsAuthorOrReadOnly(BasePermission):
    """
    Autorise la lecture à tous les contributeurs,
    mais réserve PUT/PATCH/DELETE à l'auteur de la ressource
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD et OPTIONS sont des méthodes de lecture
        if request.method in SAFE_METHODS:
            return True

        # Les modifications sont réservées à l'auteur
        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """
    Vérifie que l'utilisateur connecté est l'auteur du projet
    Utilisé pour ajouter ou supprimer des contributeurs
    """

    def has_permission(self, request, view):
        # Compatible avec routes imbriquées et routes classiques
        project_id = view.kwargs.get('project_pk') or view.kwargs.get('pk')

        if not project_id:
            return False

        return Project.objects.filter(
            id=project_id,
            author=request.user,
        ).exists()