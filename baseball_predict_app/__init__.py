from flask import Flask

def create_app():
    app = Flask(__name__)

    from baseball_predict_app.routes.baseball import main_bp
    from baseball_predict_app.routes.baseball_record import record_bp
    from baseball_predict_app.routes.baseball_predict import predict_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(record_bp)
    app.register_blueprint(predict_bp)

    return app

if __name__ == "__main__":
  app = create_app()
  app.run()