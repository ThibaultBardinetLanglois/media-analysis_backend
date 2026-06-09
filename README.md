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
