def can_trace_type(variable):
    current_type = type(variable)
    if current_type in [int, str, float, dict, type(None)]:
        return True

    print(current_type)

    return False