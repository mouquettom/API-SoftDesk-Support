# SoftDesk Support API

API RESTful sécurisée développée avec Django REST Framework dans le cadre du projet OpenClassrooms "Créez une API sécurisée RESTful avec Django REST".

## Description

SoftDesk Support est une API B2B permettant la gestion collaborative de projets techniques :

- gestion des utilisateurs
- création de projets
- gestion des contributeurs
- suivi des issues/tickets
- commentaires sur les issues
- authentification JWT sécurisée

---

## Technologies utilisées 

- Python 3
- Django
- Django REST Framework
- Simple JWT
- SQLite3

---

## Structure du projet

```text
src/
├── SoftDeskSupport/
├── users/
├── projects/
├── issues/
└── comments/
```

---

## Authentification

L’API utilise JWT (JSON Web Token).

## Obtenir un token

```http
POST /api/token/access/
```

Body :

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

---

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/mouquettom/API-SoftDesk-Support.git
```

### 2. Accéder au projet

```bash
cd API-SoftDesk-Support
```

### 3. Créer un environnement virtuel

#### macOS / Linux

```bash
python3 -m venv .env
source .env/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 5. Appliquer les migrations

```bash
cd src
python manage.py migrate
```

---

### 6. Lancer le serveur

```bash
python manage.py runserver
```

---

## Endpoints principaux

### Users

| Méthode | Endpoint | Description |
|---|---|---|
| POST | /api/users/register/ | Créer un utilisateur |
| GET | /api/users/me/ | Voir son profil |
| PATCH | /api/users/me/ | Modifier son profil |
| DELETE | /api/users/me/ | Supprimer son compte |

---

### Projects

| Méthode | Endpoint |
|---|---|
| GET | /api/projects/ |
| POST | /api/projects/ |
| GET | /api/projects/{id}/ |
| PATCH | /api/projects/{id}/ |
| DELETE | /api/projects/{id}/ |

---

### Contributors

| Méthode | Endpoint |
|---|---|
| GET | /api/projects/{project_id}/users/ |
| POST | /api/projects/{project_id}/users/ |

---

### Issues

| Méthode | Endpoint |
|---|---|
| GET | /api/projects/{project_id}/issues/ |
| POST | /api/projects/{project_id}/issues/ |

---

### Comments

| Méthode | Endpoint |
|---|---|
| GET | /api/projects/{project_id}/issues/{issue_id}/comments/ |
| POST | /api/projects/{project_id}/issues/{issue_id}/comments/ |

---

## Permissions

- authentification JWT obligatoire
- seuls les contributeurs peuvent accéder aux projets
- seul l’auteur peut modifier/supprimer son contenu
- assignation d’issues limitée aux contributeurs

---

## Fonctionnalités techniques

- routes imbriquées
- permissions personnalisées
- serializers DRF
- UUID pour les commentaires
- validation métier
- pagination
- modèle utilisateur personnalisé

---

@Tom Mouquet