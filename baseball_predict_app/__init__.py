from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

def create_app():
    app = Flask(__name__)

    from baseball_predict_app.routes.baseball import baseball

    app.register_blueprint(baseball)

    return app

if __name__ == "__main__":
  app = create_app()
  app.run()