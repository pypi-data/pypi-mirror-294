def format_float(value:float, precision:int=3) -> str:
    """Return formatted float.
    
    Args:
        value (`float`, Mandatory): Float value to be formatted.
        precision (`int`, Optional): Desired precision of the float value. Defaults to `3`.
    """
    return str(round(value,precision)).rstrip('0').rstrip('.')