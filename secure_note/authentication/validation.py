import re

def validate_password(password):
  """
  Validates password strength using regular expressions.

  Args:
      password: The password string to validate.

  Returns:
      True if the password is valid, False otherwise.
  """
  pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  if not re.search(pattern, password):
    return False
  return True