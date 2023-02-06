# Generate migrations

## To generate alembic migration you should use inside docker container

`docker exec -it docker_id /bin/bash`

`alembic revision --autogenerate -m "message"`
