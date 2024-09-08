import sys

def clear_line(line:int=1):
    """Clear printed line in terminal or output.

    Args:
        line (`int`, Optional): Amount of line to be cleared from terminal or output. Defaults to `1`.
    """
    for _ in range(line):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")