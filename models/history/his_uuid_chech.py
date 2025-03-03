from uuid import UUID, uuid4

def is_valid_uuid(uuid_to_test: str, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False
