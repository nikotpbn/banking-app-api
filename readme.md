# NextGen Bank project from Udemy course

Tech Stack:
DjangoRestFramework, Celery, Redis, PostgreSQL, NGINX

Adaptations:
 - No settings granulation in order to not modify root project files.
 - Use of docker secrets instead of env files, wich adds an extra layer of security for credentials.
 - Use of alpine image instead of Debian's Bookworm, which implicates in a massive image size reduction.
 - Different setup for Dockerfiles