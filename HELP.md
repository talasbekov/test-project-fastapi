# Generate migrations

## To generate alembic migration you should use inside docker container

### Firstly check if models are imported in **init**.py of models package

`docker exec -it docker_id /bin/bash`

`alembic revision --autogenerate -m "message"`
