from flask import Flask
from models import db
from routes import bp as controllers_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(controllers_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# app.py

# from flask import Flask
# from models import db
# from routes import bp as controllers_blueprint

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)

#     app.register_blueprint(controllers_blueprint)

#     return app


