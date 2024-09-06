""" Auxiliary functions to guarantee string and integer variables """


def evaluate_str(string, item_name):
    """Avoid empty or None strings

    :param: string: value to be evaluated
    :param: item_name: name of item to be evaluated
    :return: correct string
    """

    if not string and string != 0:
        raise ValueError(f"{item_name} cannot be empty")

    if not isinstance(string, str):
        try:
            string = str(string)
        except TypeError as exc:
            raise ValueError(f"{item_name} must be a string") from exc

    return string


def evaluate_integer(integer, item_name):
    """Evaluate if 'integer' provided is a valid integer

    :return:
        Return Integer >= 0 for valid
        Return False for invalid"""

    if integer == 0:
        return 0

    if not integer:
        raise ValueError(f"{item_name} must be an integer")

    if not isinstance(integer, int):
        try:
            integer = int(integer)
            return evaluate_integer(integer, "integer")
        except TypeError as exc:
            raise ValueError(f"{item_name} must be an integer") from exc

    if integer < 0:
        raise ValueError(f"{item_name} must be >= 0")

    return integer
