def validate_property(v: dict):

    if v is None:
        return v

    keys = list(v)
        
    for key in keys:

        value = v[key]
        if not isinstance(value, dict):
            raise ValueError("value is not dictionary")

        prefix_msg = f'In {key}: '

        types = ["read", "write"]
        type = value.get("type")
        if type is None or not isinstance(type, str) or type.lower() not in types:
            raise ValueError(prefix_msg + 'type should be either "read/write"')

        data_takens = ["auto", "manual", "dropdown", "date_picker"]
        data_taken = value.get('data_taken')
        if data_taken is None or not isinstance(data_taken, str) or data_taken not in data_takens:
            raise ValueError(prefix_msg + 'data_taken should be either "auto/manual/dropdown/date_picker"')

        alias_name = value.get('alias_name')
        if alias_name is None or not isinstance(alias_name, str):
            raise ValueError(prefix_msg + 'alias_name should be present')

        if type == "write":
            field_name = value.get('field_name')
            if field_name is None:
                raise ValueError(prefix_msg + 'field_name should not be None')
            if data_taken == "auto":
                val = value.get('value')
                if val is None:
                    raise ValueError(prefix_msg + "value should be present")
    return v
