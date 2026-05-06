from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Contributor
from .models import Issue


# Récupère le modèle utilisateur actif
User = get_user_model()


class IssueSerializer(serializers.ModelSerializer):

    # Le projet est affiché mais ne peut pas être choisi dans le body
    # Il vient de l'URL imbriquée :  /projects/{project_pk}/issues/
    project = serializers.ReadOnlyField(source='project.id')

    # L'auteur est affiché mais défini automatiquement dans la view
    author = serializers.ReadOnlyField(source='author.id')

    # Champ d'écriture : dans Postman, on envoie assignee_id
    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee',
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    # Champ de lecture : dans la réponse, on affiche l'id de l'assigné
    assignee = serializers.ReadOnlyField(source='assignee.id')

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'tag',
            'status',
            'project',
            'author',
            'assignee',
            'assignee_id',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        """
        Validation : Si un utilisateur est assigné à l'issue,
        il doit obligatoirement être contributeur du projet concerné
        """
        # project_id est transmis depuis la view via get_serializer_context()
        project_id = self.context.get('project_id')

        # Grâce à source='assignee', assignee_id devient assignee dans attrs
        assignee = attrs.get('assignee')

        # Si un assigné est fourni, on vérifie qu'il est contributeur du projet
        if assignee is not None and project_id is not None:
            is_contrib = Contributor.objects.filter(
                project_id=project_id,
                user=assignee,
            ).exists()

            if not is_contrib:
                raise serializers.ValidationError({
                    'assignee_id': (
                        "L'utilisateur assigné à cette mission doit être contributeur du projet."
                    )
                })

        return attrs