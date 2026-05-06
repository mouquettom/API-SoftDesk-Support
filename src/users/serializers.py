from django.contrib.auth import get_user_model
from rest_framework import serializers


# Récupère le modèle utilisateur actif du projet
User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """ Inscription • POST  -> transforme les données JSON reçues en objet User """

    # Ici on redéfinit password
    # write_only=True : le champ est envoyé à l'API en entrée, mais ne sera jamais renvoyé dans la réponse
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
        ]

    # On crée un nouvel utilisateur
    # 'validated_data' est un dictionnaire contenant uniquement les données validées par le serializer
    def create(self, validated_data):
        # On supprime la clé 'password' du dictionnaire
        password = validated_data.pop('password')

        # L'opérateur ** décompose un dictionnaire en arguments nommés
        user = User(**validated_data)

        # La méthode set_password() transforme le mot de passe brut en mot de passe hashé
        # C'est indispensable car on ne doit jamais stocker un mot de passe en clair
        user.set_password(password)
        # Enfin user.save() permet de sauvegarder l'utilisateur dans la base de données
        user.save()
        # On retourne l'instance créée
        return user


class PublicUserSerializer(serializers.ModelSerializer):
    """ Lecture seule (profil public) • GET """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]


class PersonalUserSerializer(serializers.ModelSerializer):
    """ Lecture seule (mon profil) • GET """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
        ]


class UpdateUserSerializer(serializers.ModelSerializer):
    """ Modification (mon profil) • PATCH """

    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'can_be_contacted',
            'can_data_be_shared',
        ]

    # Ici on met à jour les champs, puis on hashe le mot de passe si nécessaire
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # On crée une boucle qui traverse le dictionnaire validated_data
        # On entre la nouvelle valeur ou non pour chaque attribut contenu dans ce dictionnaire
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance