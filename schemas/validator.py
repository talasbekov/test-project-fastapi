VALID_TYPES = {"read", "write", "delete"}
VALID_DATA_TAKEN = {"auto", "manual", "dropdown", "date_picker", "matreshka"}

def validate_property(key: str, value: dict):
    """
    Validates a single property in the `properties` dictionary, handling default values.
    """
    if not isinstance(value, dict):
        raise ValueError(f"In {key}: Value is not a dictionary")

    prefix_msg = f"In {key}: "

    # Set default values for missing or null keys
    type_value = value.get("type", "read")  # Default to "read" if not provided
    if not isinstance(type_value, str) or type_value.lower() not in VALID_TYPES:
        raise ValueError(prefix_msg + 'type should be one of "read", "write", "delete"')

    data_taken = value.get("data_taken", None)  # value.get("data_taken", "")  - Default to "" if not provided
    if not isinstance(data_taken, str) or data_taken not in VALID_DATA_TAKEN:
        raise ValueError(
            prefix_msg + 'data_taken should be one of "auto", "manual", "dropdown", "date_picker", "matreshka"'
        )

    # Set alias_name and alias_nameKZ default to "" if missing or null
    alias_name = value.get("alias_name", "")  # Default to "" if not provided
    if alias_name is None:
        alias_name = ""
    if not isinstance(alias_name, str):
        raise ValueError(prefix_msg + 'alias_name should be a string')

    alias_nameKZ = value.get("alias_nameKZ", "")  # Default to "" if not provided
    if alias_nameKZ is None:
        alias_nameKZ = ""
    if not isinstance(alias_nameKZ, str):
        raise ValueError(prefix_msg + 'alias_nameKZ should be a string')

    # Initialize field_name with a default value
    field_name = ""  # Default to empty string

    # If type is "write", validate "field_name"
    if type_value == "write":
        field_name = value.get("field_name", "")  # Default to "" if not provided
        if not field_name:
            raise ValueError(prefix_msg + 'field_name should not be None if type is "write"')

    # Handle to_tags dictionary and set defaults for nested fields
    to_tags = value.get("to_tags", {})
    directory = to_tags.get("directory", "")  # Default to "" if not provided
    if directory is None:
        directory = ""
    
    isHidden = to_tags.get("isHidden", False)  # Default to False if not provided
    cases = to_tags.get("cases", 0)  # Default to 0 if not provided

    if data_taken in {"auto", "dropdown"}:
        data_type = None
    else:
        data_type = value.get("data_type", "")


    # Set data_type to empty string if not provided
    # data_type = value.get("data_type", "")  # Default to "" if not provided
    # if data_type is None:
    #     data_type = ""

    # Returning validated value with default values applied
    return {
        **value,
        "type": type_value,
        "data_taken": data_taken,
        "alias_name": alias_name,
        "alias_nameKZ": alias_nameKZ,
        "field_name": field_name,  # Ensure field_name is always defined
        "to_tags": {
            "directory": directory,
            "isHidden": isHidden,
            "cases": cases
        },
        "data_type": data_type
    }

def hr_document_templates_properties_validator(v: dict):
    """
    Validates the `properties` field in HrDocumentTemplateBase.
    """
    if not v:
        return v

    for key, value in v.items():
        v[key] = validate_property(key, value)

    return v


def test_validate_property(key: str, value: dict):
    """
    Validates a single property in the `properties` dictionary, handling default values.
    """
    if not isinstance(value, dict):
        raise ValueError(f"In {key}: Value is not a dictionary")

    prefix_msg = f"In {key}: "
    VALID_T = {"read", "write"}

    # Set default values for missing or null keys
    type_value = value.get("type", "read")  # Default to "read"
    if not isinstance(type_value, str) or type_value not in VALID_T:
        type_value = "read"

    data_taken = value.get("data_taken", None)  # Default to None
    if data_taken not in VALID_DATA_TAKEN:
        data_taken = "auto"  

    alias_name = value.get("alias_name", "")  # Default to empty string
    if not isinstance(alias_name, str):
        raise ValueError(prefix_msg + "alias_name should be a string")

    alias_nameKZ = value.get("alias_nameKZ", "")  # Default to empty string
    if not isinstance(alias_nameKZ, str):
        raise ValueError(prefix_msg + "alias_nameKZ should be a string")

    field_name = value.get("field_name", "") if type_value == "write" else ""
    if type_value == "write" and not field_name:
        raise ValueError(prefix_msg + "field_name is required for type 'write'")

    # Handle `to_tags` and nested fields
    to_tags = value.get("to_tags", {})
    to_tags.setdefault("directory", "")
    to_tags.setdefault("isHidden", False)
    to_tags.setdefault("cases", 0)
    to_tags.setdefault("prevWordKZ", "")

    prevWordKZ = to_tags.get("prevWordKZ", "")
    if not isinstance(prevWordKZ, str):
        raise ValueError(prefix_msg + "prevWordKZ in to_tags should be a string")

    # Validate `data_type` for specific `data_taken` values
    if data_taken in {"auto", "dropdown"}:
        data_type = None
    else:
        data_type = value.get("data_type", None)
        if data_type is not None and not isinstance(data_type, str):
            raise ValueError(prefix_msg + "data_type should be a string or None")

    # Returning validated property
    return {
        **value,
        "type": type_value,
        "data_taken": data_taken,
        "alias_name": alias_name,
        "alias_nameKZ": alias_nameKZ,
        "field_name": field_name,
        "to_tags": {
            "directory": to_tags["directory"],
            "isHidden": to_tags["isHidden"],
            "cases": to_tags["cases"],
            "prevWordKZ": prevWordKZ,
        },
        "data_type": data_type,
    }

def validate_document_property(v: dict):
    """
    Validates the `properties` field in HrDocumentTemplateBase.
    """
    if not v:
        return v

    for key, value in v.items():
        v[key] = test_validate_property(key, value)

    return v

def hr_document_properties_validator(v: dict):
    if v is None:
        return v
    if not isinstance(v, dict):
        raise ValueError('properties should be dictionary')
    keys = list(v)
    for key in keys:
        value = v[key]
        if isinstance(value, dict):
            val_keys = list(value)
            if 'name' not in val_keys or 'value' not in val_keys:
                raise ValueError(f'name or value should be in {key}!')
    return v
