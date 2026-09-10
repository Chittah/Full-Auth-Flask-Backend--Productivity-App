from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_migrate import Migrate
from extensions import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

from models import User


@app.route("/")
def home():
    return {"message": "Secure Task API is running"}


if __name__ == "__main__":
    app.run(debug=True)