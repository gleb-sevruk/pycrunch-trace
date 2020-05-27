allowed_types = [int, str, float, dict, type(None), bool]
# allowed_types = [int, str, float,  type(None), bool]


def can_trace_type(variable):
    # return False
    current_type = type(variable)
    if current_type in allowed_types:
        return True

    # print(current_type)

    return False