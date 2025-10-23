# Microservicio REST con Django (Plataforma de cursos)

## Objetivo
API REST para una plataforma de cursos en línea que gestiona **usuarios**, **cursos**, **lecciones**, **inscripciones** y **comentarios**, construida con **Django REST Framework**, documentada con **drf-yasg** (Swagger/Redoc) y ejecutable en **Docker** con **PostgreSQL**.

---

## Requisitos
- Docker y docker-compose instalados.
- Puerto `8500` disponible (puedes cambiarlo en `docker-compose.yml`).

---

## Cómo ejecutar con Docker

Construir y levantar contenedores:
   ```bash
   docker-compose up --build
   # (según tu versión también puedes usar:)
   # docker compose up --build

## Aplicar migraciones (con los contenedores arriba)

```bash
docker-compose exec web python manage.py migrate
# o:
# docker compose exec web python manage.py migrate

## Crear superusuario

docker-compose exec web python manage.py createsuperuser
# alternativa (si conoces el nombre del contenedor):
# docker exec -it <nombre-del-contenedor> python manage.py createsuperuser
# verifica el nombre con: docker ps


## Quedara disponible en http://localhost:8500/
