import os

from dotenv import load_dotenv

from app import create_app

if __name__ == '__main__':
    load_dotenv('.env')
    app = create_app(os.environ.get('CONFIG'))
    app.run()
