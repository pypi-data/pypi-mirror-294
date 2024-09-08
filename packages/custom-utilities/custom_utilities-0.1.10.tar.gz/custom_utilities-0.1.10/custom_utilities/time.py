from .number import format_float

def parse_duration(duration_in_seconds:float=0) -> str:
    """Return parsed duration.

    Args:
        duration_in_seconds (`float`, Optional): Duration to be parsed in seconds unit.
            It is suggested to use value from time or datetime methods. Defults to `0`.
    """

    # * Function Logic
    if duration_in_seconds == 0:
        return '0ms'
    elif duration_in_seconds < 1:
        return format_float(duration_in_seconds * 1000) + 'ms'
    elif duration_in_seconds < 60:
        return format_float(duration_in_seconds) + 's'
    duration_in_hours, duration_remainder = divmod(duration_in_seconds, 3600)
    duration_in_minutes, duration_in_seconds = divmod(duration_remainder, 60)
    duration_in_milliseconds = duration_in_seconds % 1 * 1000
    duration_parameters:list[str] = []
    if duration_in_hours != 0:
        duration_parameters.append(str(int(duration_in_hours)) + 'h')
    if duration_in_minutes != 0:
        duration_parameters.append(str(int(duration_in_minutes)) + 'm')
    if duration_in_seconds != 0:
        duration_parameters.append(str(int(duration_in_seconds)) + 's')
    if duration_in_milliseconds != 0:
        duration_parameters.append(str(int(duration_in_milliseconds)) + 'ms')
    return ':'.join(duration_parameters)