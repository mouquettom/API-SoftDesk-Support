from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from .serializers import CreateUserSerializer, PublicUserSerializer, \
    PersonalUserSerializer, UpdateUserSerializer


# Récupère le modèle utilisateur actif du projet
User = get_user_model()


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet de gestion des utilisateurs

    On utilise des mixins pour exposer seulement certaines actions :
    - list : voir les utilisateurs
    - retrieve : voir un utilisateur
    - destroy : suppression admin d'un utilisateur

    Les actions register et me sont ajoutées manuellement avec @action
    """

    def get_serializer_class(self):
        """ Détermine le serializer à utiliser selon l'action """
        # POST      /users/register/
        if self.action == 'register':
            return CreateUserSerializer

        # GET       /users/  &  /users/<pk>/
        if self.action in ['list', 'retrieve']:
            return PublicUserSerializer

        # PATCH     /users/me/
        if self.action == 'me':
            if self.request.method == 'PATCH':
                return UpdateUserSerializer
            return PersonalUserSerializer

        # GET       /users/me/
        return PersonalUserSerializer

    def get_permissions(self):
        """ Qui a les droits ? """
        # L'inscription est publique : pas besoin d'être connecté
        if self.action == 'register':
            return [AllowAny()]

        # Suppression via  /users/{id}/  réservée à l'admin uniquement
        if self.action == 'destroy':
            return [IsAdminUser()]

        # Toutes les autres actions nécessitent un JWT valide
        return [IsAuthenticated()]

    def get_queryset(self):
        """ Retourne la liste des utilisateurs """
        # Par défaut, seuls les comptes actifs sont visibles
        queryset = User.objects.all().order_by('id')

        # Pour destroy, l'admin peut aussi cibler un compte inactif
        if self.action == 'destroy':
            return queryset

        return queryset.filter(is_active=True)

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        """
        Route personalisée :
        POST    /api/users/register/   → inscription
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # On retourne le profil personnel sans afficher le mot de passe
        return Response(
            PersonalUserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @action(methods=['get', 'patch', 'delete'], detail=False, url_path='me')
    def me(self, request):
        """
        Routes personalisées :
        GET     /api/users/me/        → voir mon profil
        PATCH   /api/users/me/        → modifier mon profil
        DELETE  /api/users/me/        → supprimer mon compte
        """
        user = request.user

        # Voir mon profil
        if request.method == 'GET':
            return Response(PersonalUserSerializer(user).data)

        # Modifier mon profil
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_user = serializer.save()
            return Response(PersonalUserSerializer(updated_user).data, status=status.HTTP_200_OK)

        # Droit à l'oubli : suppression du compte
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)