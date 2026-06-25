# media-analysis_backend

media-analysis-backend
│
├── app
│ ├── api
│ │ └── v1
│ │ ├── router.py
│ │ ├── health.py
│ │ ├── media.py
│ │ └── search.py
│ │
│ ├── core
│ │ ├── config.py
│ │ ├── database.py
│ │ └── security.py
│ │
│ ├── models
│ │ ├── media.py
│ │ ├── extracted_text.py
│ │ └── keyword.py
│ │
│ ├── schemas
│ │ ├── media.py
│ │ └── search.py
│ │
│ ├── repositories
│ │ ├── media_repository.py
│ │ └── search_repository.py
│ │
│ ├── services
│ │ ├── media_service.py
│ │ ├── search_service.py
│ │ └── processors
│ │ ├── base_processor.py
│ │ ├── text_processor.py
│ │ ├── image_processor.py
│ │ ├── audio_processor.py
│ │ └── video_processor.py
│ │
│ ├── tests
│ │
│ └── main.py
│
├── uploads
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .env.example
├── README.md
└── .gitignore

# commits

1 - git commit -m "feat(init): bootstrap FastAPI project with Docker, PostgreSQL, pgAdmin and healthcheck"
2 - git commit -m "feat(config): add settings management and database configuration"
3 - git commit -m "feat(media): add media domain model and repository layer"
4 - git commit -m "feat(upload): implement media upload endpoint"
5 - git commit -m "feat(processors): introduce processor strategy architecture for text, image, audio, and video"
6 - git commit -m "feat(text-processing): implement text file processing and keyword extraction"
7 - git commit -m "feat(search): implement keyword search endpoint"
8 - git commit -m "feat(image-processing): add OCR processing pipeline for image files"
9 - git commit -m "feat(video-processing): add video ingestion workflow"
10 - git commit -m "test(api): add backend unit and integration tests"

# Schéma global :

media-analysis-frontend
React + Vite
|
| HTTP
v
media-analysis-backend
FastAPI
|
| SQLAlchemy
v
PostgreSQL + pgAdmin

# Flux :

Upload fichier texte
↓
Backend stocke le fichier sur disque
↓
Crée une ligne media
↓
Extrait le texte
↓
Extrait les mots-clés
↓
Insère extracted_text + keywords
↓
Recherche possible depuis React

# pgAdmin :

Dans pgAdmin, pour connecter PostgreSQL, on remplit les champs de connexion avec les valeurs suivantes (en fonction de ce qui est défini dans le docker-compose.yml et le .env) :

Host: db
Port: 5432
Username: POSTGRES_USER
Password: POSTGRES_PASSWORD
Database: POSTGRES_DB

Penser à nommer le "server Name" dans pgAdmin pour éviter les confusions, par exemple "media-analysis-db".

# Commandes utiles :

# Docker

- Crée les réseaux et volumes si nécessaire.
- Construit les images si elles n'existent pas déjà.
- Crée et démarre les conteneurs définis dans docker-compose.yml.
- Affiche les logs en temps réel.
  docker compose up

- Reconstruit les images avant de démarrer.
  docker compose up --build

- Reconstruire les images
  docker compose build --no-cache

    Le --no-cache force une reconstruction complète.

- Arrêter et supprimer les conteneurs + volumes
  docker compose down -v

- Lorsque tu veux vraiment repartir d'un environnement complètement propre.
  docker compose down -v --rmi local

    down → arrête et supprime les conteneurs du projet.
    -v → supprime aussi les volumes (⚠️ donc les données PostgreSQL sont perdues).
    --rmi local → supprime les images Docker construites localement par ton projet (pas les images téléchargées comme postgres ou pgadmin, sauf si elles sont considérées comme locales et sans tag personnalisé).

# Curl

- Tester le healthcheck de l'API :
  curl -X GET "http://localhost:8000/api/v1/health"

- Tester l'upload d'un fichier texte :
  curl -X POST "http://localhost:8000/api/v1/media/upload" -F "file=@fileName"

- Tester l'upload d'un fichier texte ayant un mauvais nomm :
  curl -F "file=@sample.txt;filename=../../evil.txt"

# Créer un fichier d'une taille spécifique pour tester la limite de taille d'upload (en octets) :

yes "hello world" | head -c 2M > big.txt

La commande yes affiche indéfiniment la chaîne passée en argument, suivie d'un retour à la ligne.

Elle produit un flux comme :

hello world
hello world
hello world
hello world
...

Le pipe (|) envoie la sortie de yes vers la commande suivante.
head lit uniquement les 2 mégaoctets (2 × 1024 × 1024 = 2 097 152 octets) du flux entrant, puis s'arrête.

-c : compter en octets
2M : 2 mébioctets (2 × 1024²)

Lorsque head a lu ces 2 MiB, il termine. La commande yes reçoit alors un signal indiquant que le tube est fermé et s'arrête également.

> big.txt

Redirige la sortie de head dans le fichier big.txt, qui sera créé s'il n'existe pas, ou écrasé s'il existe déjà.
