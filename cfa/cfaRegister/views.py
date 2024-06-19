from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CfaUser
from .serializers import CfaUserSerializer

# Importation du module pour la génération de tokens JWT
from rest_framework_simplejwt.tokens import RefreshToken

# On définit un ViewSet pour le modèle CfaUser
class CfaUserViewSet(viewsets.ModelViewSet):
    # On définit de la queryset qui va récupérer tous les objets CfaUser
    queryset = CfaUser.objects.all()

    # On spécifie le serializer à utiliser pour ce ViewSet
    serializer_class = CfaUserSerializer

    # On définit une action personnalisée pour l'enregistrement des CFA
    @action(detail=False, methods=['post'], url_path='register-cfa')
    def register_cfa(self, request):
        # Récupération des données de la requête et création du serializer
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # On génére un token JWT pour l'utilisateur nouvellement créé
            refresh = RefreshToken.for_user(user)

            # Retourner une réponse avec les détails de l'utilisateur et le token
            return Response({
                'email': user.email,
                'denomination': user.denomination,
                'siretNumber': user.siretNumber,
                'cfaToken': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        # Retourner une réponse avec les erreurs de validation si les données sont invalides
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)