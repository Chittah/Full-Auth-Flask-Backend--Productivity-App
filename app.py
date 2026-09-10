from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask, request
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

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"message": "Username, email and password are required"}, 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return {"message": "Username or email already exists"}, 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, 201

if __name__ == "__main__":
    app.run(debug=True)