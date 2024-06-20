from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import uuid
from .models import CfaUser, sendStudentInvitation
from .serializers import CfaUserSerializer, sendStudentInvitationSerializer

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
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # On récupére les données de la requête POST
        email = request.data.get('email')
        password = request.data.get('password')
            
        # On authentifier le cfa avec l'email et le mot de passe
        user = authenticate(email=email, password=password)

        if user:
            # On génére un token JWT pour le cfa authentifié
            refresh = RefreshToken.for_user(user)
            return Response({
                'email': user.email,
                'denomination': user.denomination,
                'siretNumber': user.siretNumber,
                'cfaToken': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"détail": "Identifiants non valides"}, status=status.HTTP_401_UNAUTHORIZED)
        
class InvitationViewSet(viewsets.ViewSet):
    # Seuls les utilisateurs authentifiés peuvent envoyer des invitations
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add-newstudent')
    def add_newstudent(self, request):
        # On crée un serializer avec les données de la requête
        serializer = sendStudentInvitationSerializer(data=request.data)
        if serializer.is_valid():
            # On génére un token unique pour l'invitation
            token = str(uuid.uuid4())
            # Enregistrer l'invitation avec les données validées
            serializer.save(cfa=request.user, token=token)
            # Retourner le token dans la réponse 
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)