from common.app_initialization import create_app


app = create_app()


@app.get("/")
def hello_world():
    return {"hello": "world"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
