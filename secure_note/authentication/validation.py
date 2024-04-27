import re

def validate_password(password:str) -> bool:
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

def filter_input(input_text:str) -> str:
  pass

def is_all_char(message:str) -> bool:
  return all(i.isalpha() for i in message)

def is_all_char_num(message:str)->bool:
  return all(i.isalpah() or i.isdigit() for i in message)

