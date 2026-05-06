from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, Contributor


# Récupère le modèle utilisateur actif du projet
User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializer pour lire, créer et modifier un projet """

    # L'auteur est affiché mais ne peut pas être choisi par l'utilisateur
    author = serializers.ReadOnlyField(source='author.id')

    # Champ calculé : indique si l'utilisateur connecté est l'auteur du projet
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author',
            'is_author',
            'created_at',
            'updated_at',
        ]

    def get_is_author(self, obj):
        # Récupère la requête envoyée automatiquement dans le contexte du serializer
        request = self.context.get('request')

        # Retourne True si l'utilisateur connecté est l'auteur du projet
        return bool(
            request
            and request.user.is_authenticated
            and obj.author.id == request.user.id
        )


class ContributorSerializer(serializers.ModelSerializer):
    """ Serializer pour lister ou ajouter des contributeurs """

    # Champ utilisé en écriture : on envoie user_id dans Postman
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        write_only=True,
    )
    # Champ utilisé en lecture : affiche l'id de l'utilisateur contributeur
    user = serializers.ReadOnlyField(source='user_id')

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'user_id',
            'project',
            'created_at'
        ]
        # Le projet ne vient pas du body, mais de l'URL imbriquée
        read_only_fields = ['project']