""" Constants for the users entities. """

PASS_REGEX_PATTERN = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
    r"(?=.*[@$!%*#?&+\-_.;,])[A-Za-z\d@$!#%*?&+\-_.;,]{6,20}$"
)
