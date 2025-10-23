# Microservicio REST con Django (Plataforma de cursos)

## Objetivo
API REST para una plataforma de cursos en línea que gestiona **usuarios**, **cursos**, **lecciones**, **inscripciones** y **comentarios**, construida con **Django REST Framework**, documentada con **drf-yasg** (Swagger/Redoc) y ejecutable en **Docker** con **PostgreSQL**.

---

## Requisitos
- Docker y docker-compose instalados.
- Puerto `8500` disponible en tu máquina (puedes cambiarlo en `docker-compose.yml`).

---

## Cómo ejecutar con Docker

1. Construir y levantar contenedores:
   ```bash
   docker-compose up --build
   
2. Aplicar migraciones (con los contenedores arriba):

docker-compose exec web python manage.py migrate



