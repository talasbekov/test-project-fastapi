# Admin user to Log in:

`"email":` `"admin@mail.com",`
`"password":` `"123456"`

# Generate migrations

## To generate alembic migration you should use inside docker container

### Firstly check if models are imported in **init**.py of models package

`docker compose run sgo-erp alembic revision --autogenerate -m "Message"`