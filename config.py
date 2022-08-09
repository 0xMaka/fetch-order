from os import getenv
from dotenv import load_dotenv

load_dotenv()
def get_secret(secret): 
  return getenv('SECRET')
