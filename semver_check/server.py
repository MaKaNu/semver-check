import re


def is_valid_semver(version: str) -> bool:
    """Test if the provided version is following SemVer pricinipals.

    For now a simple but rather complicated to read regex is used.
    TODO: Use the Backus-Naur Form as input an validate hirachic.

    Args:
        version (str): provided version number to check

    Returns:
        bool: weather the verion is following SemVer principals or not.
    """
    semver_regex = re.compile(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
        r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
    )
    return bool(semver_regex.match(version))
