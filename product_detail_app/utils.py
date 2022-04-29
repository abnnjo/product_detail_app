from models.exceptions import ValidationError

def get_filter_validated_data(request_data: dict, validated_data: dict) -> dict:
    """
    This function used to filter requested data
    """
    if not validated_data:
        raise ValidationError("input data (validated_data)cannot be empty")

    data = validated_data.copy()
    for key in list(validated_data):
        if not key in request_data:
            data.pop(key)
    return data
