from ckan import types


def is_ranged_float(
    key: types.FlattenKey,
    data: types.FlattenDataDict,
    errors: types.FlattenErrorDict,
    context: types.Context,
):
    """Validate that a value is a float within the inclusive range from 0.0 to 1.0]."""
    try:
        value = float(data[key])
    except ValueError:
        errors[key].append("Invalid value, should be a number.")
        return None
    if not (0 <= value and value <= 1):
        errors[key].append("Invalid value, should be in ​​range from 0.0 to 1.0.")
        return None
