import os
import dotenv


if os.environ.get('ENV', None) is None:
    dotenv.load_dotenv()

os.environ['ENV'] = os.environ['ENV'].upper()
environ = os.environ
