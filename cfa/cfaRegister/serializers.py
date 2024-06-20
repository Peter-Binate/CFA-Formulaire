from rest_framework import serializers
from .models import CfaUser, sendStudentInvitation

class CfaUserSerializer(serializers.ModelSerializer):
    # Champ pour la confirmation du mot de passe
    confirm_password = serializers.CharField(write_only=True)

    # Meta spécifie quel modèle le serializer utilise pour les opérations de sérialisation
    class Meta:
        # On associe ce serializer au modèle CfaUser
        model = CfaUser

        # On précise les champs que l'on souhaite inclure dans le serializer
        fields = ['email', 'denomination', 'password', 'confirm_password', 'siretNumber']

        # On empêche le password d'être retouné lors de la réponse de l'API
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_siretNumber(self, value):
        if not value.isdigit() or len(value) != 14:
            raise serializers.ValidationError('Le numéro de SIRET doit contenir exactement 14 chiffres.')
        return value
    
    def validate(self,  data):
        # On vérifie que les mots de passe sont identiques
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne sont pas identiques")
        return data
    
    def create(self, validated_data):
        # On supprime le champ confirm_password qui n'est pas un champ du modèle
        validated_data.pop('confirm_password')

        # On créer l'utilisateur avec les données restantes
        user = CfaUser.objects.create_user(**validated_data)

        return user 

class sendStudentInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = sendStudentInvitation
        fields = ['email', 'lastname', 'firstname']
