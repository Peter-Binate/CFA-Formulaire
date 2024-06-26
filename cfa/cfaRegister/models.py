from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone

class UserManager(BaseUserManager):
    #On crée une méthode pour créer un utilisateur standard
    def create_user(self, email, password=None, **extra_fields):
        
        # Si l'email n'est pas fournis
        if not email:
            raise ValueError('Merci de renseigner votre email')
        
        # On convertis l'email en minuscule
        email = self.normalize_email(email)
        
        # On crée l'utilisateur
        user = self.model(email=self.normalize_email(email), **extra_fields)

        #On hash le mot de passe de l'utilisateur
        user.set_password(password)

        # On save l'utilisateur dans la base de données
        user.save(using=self._db)
        return user

class CfaUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    denomination = models.CharField(max_length=255)
    siretNumber = models.CharField(max_length=14, unique=True, validators=[RegexValidator(regex='^\d{14}$', message='Le numéro de SIRET doit contenir exactement 14 chiffres.')])
    password = models.CharField(max_length=128)

    # On lie le gestionnaire personnalisé (UserManager(BaseUserManager)) à ce modèle
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['denomination', 'siretNumber']

    # On affiche l'utilisateur sous forme de chaîne de caractères
    def __str__(self):
        return self.email
    
# On récupére le modèle utilisateur actuellement utilisé
User = get_user_model()

class sendStudentInvitation(models.Model):
    # On génére un token unique pour l'invitation
    token = models.CharField(max_length=255, unique=True)
    # L'invitation est liée à un CFA
    cfa = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    invitation_accepted = models.BooleanField(default=False)
    social_security_number = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Représentation de l'invitation en chaîne de caractères
    def __str__(self):
        return f"Invitation pour {self.email} de {self.cfa.email}"