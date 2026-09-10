# Secure Task API – Productivity App

## Project Description

This project is a secure Flask REST API backend for a productivity application. The application will allow authenticated users to create and manage their own tasks.

The backend is being developed as a group project for the **Moringa School Module 5 Summative Group Project**.

The project uses Flask, SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-RESTful, Marshmallow, and SQLite. The application is structured to support authentication, user-specific resources, CRUD operations, validation, pagination, and secure authorization.

---

## Current Development Status

The project foundation has been completed on the `feature/project-setup` branch.

### Completed

* Flask application setup
* Python virtual environment setup
* SQLAlchemy database configuration
* SQLite database setup
* User model creation
* User database migration
* Flask-Migrate configuration
* Database migration and upgrade
* Project dependency management using Pipenv
* `.gitignore` configuration
* Initial application route
* Verification of the User model and database connection
* Git feature branch setup

### To Be Completed by the Group

* User registration
* Password hashing with Flask-Bcrypt
* User login and authentication
* Authentication/session or JWT management
* User logout
* Current-user/session checking
* Task model
* Task CRUD operations
* User authorization
* Marshmallow schemas and validation
* Pagination
* Seed data
* Automated tests
* Complete API documentation

---

# Technologies Used

The project uses the following technologies:

* **Python 3.8.13**
* **Flask 2.2.2**
* **Flask-SQLAlchemy 3.0.3**
* **Flask-Migrate 4.0.0**
* **Flask-RESTful 0.3.9**
* **Flask-Bcrypt 1.0.1**
* **Marshmallow 3.20.1**
* **Faker 15.3.2**
* **Werkzeug 2.2.2**
* **SQLite**
* **Pipenv**
* **Git and GitHub**
* **Pytest**

---

# Project Structure

The current project structure is:

```text
Full-Auth-Flask-Backend--Productivity-App/
│
├── app.py
├── models.py
├── schemas.py
├── seed.py
├── README.md
├── Pipfile
├── Pipfile.lock
├── requirements.txt
├── .gitignore
├── .python-version
│
├── migrations/
│   ├── versions/
│   │   └── d662e071430d3_create_user_table.py
│   └── ...
│
└── instance/
    └── app.db
```

The `instance/` directory and database file are excluded from Git through `.gitignore`.

---

# Environment Setup

The project uses Python 3.8.13.

The Python version was selected because the required Flask version is compatible with this environment and avoids compatibility problems encountered with newer Python versions.

The project uses a virtual environment:

```bash
python -m venv venv
```

Activate it with:

```bash
source venv/bin/activate
```

---

# Installing Dependencies

The project uses Pipenv for dependency management.

Install the dependencies using:

```bash
pipenv install
```

The project also maintains a `requirements.txt` file containing the installed Python packages.

To generate the requirements file from the active environment:

```bash
pip freeze > requirements.txt
```

---

# Database Configuration

The Flask application uses SQLite as the development database.

The database configuration in `app.py` is:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```

Because Flask-SQLAlchemy uses the Flask instance directory for the relative SQLite path, the database is created at:

```text
instance/app.db
```

---

# SQLAlchemy Setup

SQLAlchemy is initialized in `app.py`:

```python
db = SQLAlchemy(app)
```

Flask-Migrate is also initialized:

```python
migrate = Migrate(app, db)
```

This allows database schema changes to be tracked through migration files rather than manually modifying the database.

---

# User Model

The initial `User` model has been created in `models.py`.

The model contains:

* `id`
* `username`
* `email`
* `password_hash`

The username and email fields are unique and cannot be empty.

The password is represented by a `password_hash` field rather than storing a plain-text password.

The current model is:

```python
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )
```

Password hashing functionality will be implemented as part of the authentication component.

---

# Database Migration

Flask-Migrate was initialized and a migration was created for the User model.

The migration command used was:

```bash
flask db migrate -m "Create user table"
```

The migration detected the new `users` table and created:

```text
migrations/versions/d662e071430d3_create_user_table.py
```

The migration was then applied using:

```bash
flask db upgrade
```

The migration completed successfully.

The current migration status was verified using:

```bash
flask db current
```

which returned:

```text
d662e071430d3 (head)
```

The migration history was also verified:

```bash
flask db history
```

which showed:

```text
<base> -> d662e071430d3 (head), Create user table
```

Therefore, the database is currently at the latest migration.

---

# Testing the User Model

The User model was tested through the Flask shell.

Start the Flask shell:

```bash
flask shell
```

Import the model:

```python
from models import User
```

Then query the database:

```python
User.query.all()
```

The result was:

```python
[]
```

This is the expected result because no users have been created yet.

The successful query confirms that:

* The User model can be imported.
* SQLAlchemy is connected correctly.
* The database is accessible.
* The `users` table has been created successfully.

Exit the Flask shell with:

```python
exit()
```

---

# Initial Flask Route

The application currently has a basic route for confirming that the API is running:

```python
@app.route("/")
def home():
    return {"message": "Secure Task API is running"}
```

Running the application and visiting the root endpoint returns:

```json
{
    "message": "Secure Task API is running"
}
```

This provides a simple health check for the backend.

---

# Running the Application

Activate the virtual environment:

```bash
source venv/bin/activate
```

Then run:

```bash
python app.py
```

The Flask development server should start.

Alternatively:

```bash
flask run
```

The API can then be accessed through the local Flask development server.

---

# Database Migration Commands

### Create a migration

After changing a model:

```bash
flask db migrate -m "Describe your changes"
```

### Apply migrations

```bash
flask db upgrade
```

### Check the current migration

```bash
flask db current
```

### View migration history

```bash
flask db history
```

---

# Git Workflow

The project uses feature branches so that group members can work independently without directly modifying the `main` branch.

The project setup work was completed on:

```text
feature/project-setup
```

The intended workflow is:

```text
main
 │
 ├── feature/project-setup
 ├── feature/authentication
 ├── feature/task-model
 ├── feature/task-crud
 ├── feature/schemas-pagination
 └── feature/testing-documentation
```

Each group member works on their assigned feature branch, commits their changes, pushes the branch to GitHub, and creates a pull request for integration into `main`.

---

# Security Considerations

The final application is intended to implement the following security practices:

* Passwords must not be stored as plain text.
* Passwords will be hashed using Flask-Bcrypt.
* Protected endpoints will require authentication.
* Users will only be allowed to access their own tasks.
* Users will not be allowed to modify or delete another user's tasks.
* Database relationships will associate tasks with their owning users.
* Input validation will be implemented before data is stored.

---

# Planned Task API

The main resource for this productivity application is **Tasks**.

Each task will belong to a specific authenticated user.

The planned Task model will contain an ownership relationship through:

```text
user_id → users.id
```

The API will support the following operations:

| Method | Endpoint      | Purpose                                 |
| ------ | ------------- | --------------------------------------- |
| GET    | `/tasks`      | Retrieve the authenticated user's tasks |
| POST   | `/tasks`      | Create a new task                       |
| PATCH  | `/tasks/<id>` | Update an existing task                 |
| DELETE | `/tasks/<id>` | Delete an existing task                 |

The `GET /tasks` endpoint will support pagination.

Authentication and authorization will ensure that users can only access their own tasks.

---

# Expected Authentication Endpoints

The final authentication component is expected to provide endpoints similar to:

| Method | Endpoint  | Purpose                                       |
| ------ | --------- | --------------------------------------------- |
| POST   | `/signup` | Create a new user                             |
| POST   | `/login`  | Authenticate a user                           |
| GET    | `/me`     | Retrieve the authenticated user's information |
| POST   | `/logout` | Log out the authenticated user                |

The exact implementation may depend on whether the group uses session-based authentication or JWT authentication.

---

# Team Development Responsibilities

The project has been divided into separate components to allow parallel development.

### Project Setup

Responsible for:

* Flask setup
* Database configuration
* User model
* Flask-Migrate
* Initial migration
* Dependencies
* Git foundation

### Authentication

Responsible for:

* Signup
* Login
* Logout
* Password hashing
* Authentication protection
* Current-user functionality

### Task Model

Responsible for:

* Task model
* User-task relationship
* Task fields
* Task migration

### Task CRUD

Responsible for:

* Creating tasks
* Reading tasks
* Updating tasks
* Deleting tasks
* User authorization

### Schemas and Pagination

Responsible for:

* Marshmallow schemas
* Serialization
* Validation
* Pagination

### Testing and Documentation

Responsible for:

* API tests
* Authentication tests
* Task CRUD tests
* Integration testing
* Final documentation

---

# Current Status

The **project foundation is complete**.

The database has been successfully created, the User model has been migrated, and the migration has been verified.

The next development stage is authentication and the Task resource.

---

# Contributors

This is a collaborative Moringa School Module 5 project developed by the group members.

Each contributor is working on a separate feature branch and will merge completed work into the main project through GitHub pull requests.
