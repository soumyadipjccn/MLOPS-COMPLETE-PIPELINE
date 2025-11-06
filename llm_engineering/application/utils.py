def split_user_full_name(user_full_name: str) -> tuple[str, str]:
    """Splits a full name into first and last names.

    Args:
        user_full_name: The full name of the user.

    Returns:
        A tuple containing the first name and last name.
    """
    parts = user_full_name.split(" ", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return parts[0], ""
