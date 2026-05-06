from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer utilisé pour lire, créer et modifier un commentaire """

    # L'issue est affichée mais ne peut pas être choisie dans le body
    # Elle vient de l'URL imbriquée
    issue = serializers.ReadOnlyField(source='issue.id')

    # L'auteur est affiché mais défini automatiquement dans la view
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = [
            'id',
            'description',
            'issue',
            'author',
            'created_at',
        ]