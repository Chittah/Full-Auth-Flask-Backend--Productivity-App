from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from extensions import db
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

from models import User, Task


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


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"message": "Email and password are required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"message": "Invalid email or password"}, 401

    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"message": "Invalid email or password"}, 401

    access_token = create_access_token(identity=user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()

    return {
        "message": "You are authenticated",
        "user_id": user_id
    }, 200


# Fetch logged-in user's tasks
@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user_id).all()
    
    results = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(task, "created_at") and task.created_at else None,
            "user_id": task.user_id
        }
        for task in tasks
    ]
    return jsonify(results), 200


# Create a task
@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    if not data.get("title"):
        return {"message": "Title is required"}, 400

    due_date = None
    if data.get("due_date"):
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    new_task = Task(
        title=data.get("title"),
        description=data.get("description", ""),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        due_date=due_date,
        user_id=current_user_id  # Enforces ownership
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "priority": new_task.priority,
            "user_id": new_task.user_id
        }
    }, 201


# Fetch single task
@app.route("/tasks/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=current_user_id).first()

    if not task:
        return {"message": "Task not found or access denied"}, 404

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
        "user_id": task.user_id
    }, 200


#Update a task
@app.route("/tasks/<int:id>", methods=["PATCH"])
@jwt_required()
def update_task(id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=current_user_id).first()

    if not task:
        return {"message": "Task not found or access denied"}, 404

    data = request.get_json() or {}

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "priority" in data:
        task.priority = data["priority"]
    if "due_date" in data:
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data["due_date"] else None

    db.session.commit()
    return {"message": "Task updated successfully"}, 200


#Delete a task
@app.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=current_user_id).first()

    if not task:
        return {"message": "Task not found or access denied"}, 404

    db.session.delete(task)
    db.session.commit()
    return {"message": "Task deleted successfully"}, 200


if __name__ == "__main__":
    app.run(debug=True)
