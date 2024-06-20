# Projet de gestion des étudiants - CFA

Ce projet est développé en utilisant Django, Django REST Framework, Postman, Github et Docker pour gérer les inscriptions et les connexions des Centres de Formation d'Apprentis (CFA) ainsi que l'invitation et l'inscription des étudiants.

## Fonctionnalités
1. Inscription et connexion du CFA
2. Ajout et invitation d'un étudiant par le CFA
3. Inscription de l'étudiant avec des informations supplémentaires

## Prérequis

- Python 3.9 ou supérieur
- Docker (optionnel)
- Postman pour les tests d'API

## Installation

### Étape 1 : Cloner le dépôt

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### Étape 2 : Configurer l'environnement virtuel

```bash
python -m venv env
source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
pip install -r requirements.txt
```

### Étape 3 : Configurer la base de données

Par défaut, le projet utilise SQLite. Aucune configuration supplémentaire n'est nécessaire pour SQLite. Si vous souhaitez utiliser PostgreSQL, mettez à jour `settings.py` avec les informations appropriées.

### Étape 4 : Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Étape 5 : Démarrer le serveur de développement

```bash
python manage.py runserver
```

### Étape 6 : Utiliser Docker (optionnel)

Si vous préférez utiliser Docker, assurez-vous que Docker et Docker Compose sont installés, puis exécutez :

```bash
docker-compose up --build
```

## Routes API

### Inscription du CFA

**URL** : `http://127.0.0.1:8000/register-cfa/`

**Méthode** : `POST`

**Données** :
```json
{
    "email": "email@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "denomination": "Nom du CFA",
    "siretNumber": "12345678901234"
}
```

**Réponse** :
```json
{
    "email": "email@example.com",
    "denomination": "Nom du CFA",
    "siretNumber": "12345678901234",
    "cfaToken": "generated_token"
}
```

### Connexion du CFA

**URL** : `http://127.0.0.1:8000/login/`

**Méthode** : `POST`

**Données** :
```json
{
    "email": "email@example.com",
    "password": "password123"
}
```

**Réponse** :
```json
{
    "email": "email@example.com",
    "denomination": "Nom du CFA",
    "siretNumber": "12345678901234",
    "cfaToken": "generated_token"
}
```

### Invitation d'un étudiant

**URL** : `http://127.0.0.1:8000/invite/add-newstudent/`

**Méthode** : `POST`

**Données** :
```json
{
    "email": "student@example.com",
    "lastname": "Nom",
    "firstname": "Prénom"
}
```

**Réponse** :
```json
{
    "token": "invitation_token"
}
```

### Inscription d'un étudiant

**URL** : `http://127.0.0.1:8000/student-register/`

**Méthode** : `POST`

**Données** :
```json
{
    "token": "invitation_token",
    "social_security_number": "123456789012345",
    "birthdate": "2000-01-01",
    "address": "123 Rue Exemple"
}
```

**Réponse** :
```json
{
    "message": "Inscription réussie!"
}
```

## Tests avec Postman

1. Ouvrez Postman et créez une nouvelle collection.
2. Ajoutez les requêtes ci-dessus dans la collection.
3. Pour les requêtes nécessitant une authentification, ajoutez un en-tête `Authorization` avec la valeur `Bearer <votre_token>`.

## Dockerisation

### Dockerfile

```dockerfile
# Utiliser l'image officielle Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /app/

# Installer les dépendances à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . /app/

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Définir la commande par défaut pour exécuter l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DB_NAME=sqlite3
      - DB_PATH=/app/db.sqlite3
```

### Commandes Docker

1. Construisez l'image Docker :
```bash
docker-compose build
```

2. Démarrez les conteneurs Docker :
```bash
docker-compose up
```

Votre application sera disponible à l'adresse `http://127.0.0.1:8000`.



## Projet réaliser par Peter Binate
## Contact 
Si vous souhaitez me contacter, vous pouvez m'envoyer un email à [peter.binatel@gmail.com](mailto:peter.binatel@gmail.com).


