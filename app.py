from flask import Flask

flask = Flask(__name__)


@flask.get("/")
def home():
    return {"message": "hello"}


# if __name__ == "__main__":
#     flask.run(port=8080)
