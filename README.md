# SECURE FLASK REST API BACKEND

## Task Management System

---

## 1. Project Title

**Secure Flask REST API Backend – Task Management System**

A secure RESTful backend API developed using Python Flask for managing users and their tasks. The system provides user registration, authentication, authorization, task management, validation, pagination, password hashing, JWT-based security, database migrations, and automated testing.

---

# 2. Project Overview

The Task Management System is a backend REST API that allows registered users to securely create, view, update, and delete their personal tasks.

The system was developed as a collaborative Flask project with the main objective of demonstrating practical implementation of:

* Flask REST APIs
* SQLAlchemy database modelling
* User authentication
* JWT authorization
* Password hashing
* CRUD operations
* Ownership-based access control
* Marshmallow validation
* Pagination
* Database migrations
* Automated testing
* Git and GitHub collaboration

The application separates users and their tasks so that every task belongs to a particular authenticated user.

A user can only access and modify tasks that belong to them.

---

# 3. Problem Statement

Task management applications need to protect user information and ensure that one user cannot access another user's private tasks.

A simple task API that does not implement authentication and authorization can expose serious security vulnerabilities. For example:

* An unauthenticated person could create tasks.
* A user could access another user's tasks.
* Passwords could be stored in plain text.
* Invalid data could be inserted into the database.
* Large numbers of tasks could be returned in one request.
* API endpoints could be accessed without proper authorization.

This project addresses these problems by implementing authentication, authorization, validation, secure password storage, ownership controls, and pagination.

---

# 4. Project Objectives

## 4.1 Main Objective

To develop a secure and tested Flask REST API for managing users and their personal tasks.

## 4.2 Specific Objectives

The project aims to:

1. Develop a Flask-based REST API.
2. Implement user registration.
3. Secure user passwords using hashing.
4. Implement JWT-based authentication.
5. Protect private API endpoints.
6. Create a relational database using SQLAlchemy.
7. Implement User and Task models.
8. Establish a one-to-many relationship between users and tasks.
9. Implement CRUD operations for tasks.
10. Restrict task access to the task owner.
11. Validate incoming task data.
12. Implement pagination.
13. Implement database migrations using Flask-Migrate.
14. Develop automated tests using pytest.
15. Document the API and installation process.
16. Use Git and GitHub for collaborative development.

---

# 5. Technologies Used

| Technology         | Purpose                              |
| ------------------ | ------------------------------------ |
| Python             | Main programming language            |
| Flask              | Web application framework            |
| Flask-SQLAlchemy   | Database ORM                         |
| SQLAlchemy         | Database interaction                 |
| SQLite             | Development/test database            |
| Flask-Migrate      | Database migrations                  |
| Alembic            | Migration engine                     |
| Flask-Bcrypt       | Password hashing                     |
| Flask-JWT-Extended | JWT authentication                   |
| Marshmallow        | Data validation and serialization    |
| Pytest             | Automated testing                    |
| Git                | Version control                      |
| GitHub             | Collaborative source-code management |
| VS Code            | Development environment              |
| WSL Ubuntu         | Development environment              |

---

# 6. System Architecture

The application follows a layered REST API architecture.

```text
                    CLIENT
                      |
                      |
                 HTTP REQUEST
                      |
                      v
              +---------------+
              | Flask Routes  |
              +---------------+
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Authentication           Validation
       JWT                  Marshmallow
          |                       |
          +-----------+-----------+
                      |
                      v
                Application
                   Logic
                      |
                      v
               SQLAlchemy ORM
                      |
                      v
                  Database
                      |
                      v
                 SQLite DB
```

The client communicates with the Flask API through HTTP requests.

The Flask routes receive requests and determine which operation needs to be performed.

Authentication verifies the user's JWT.

Marshmallow validates incoming data.

SQLAlchemy communicates with the database.

The database stores users and tasks.

---

# 7. Project Structure

The project is organized approximately as follows:

```text
Full-Auth-Flask-Backend--Productivity-App/
│
├── app.py
├── models.py
├── schemas.py
├── extensions.py
├── migrations/
│
├── testing/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
│
├── instance/
│   └── app.db
│
├── venv/
│
├── requirements.txt
└── README.md
```

## Important files

### app.py

Contains:

* Flask application
* configuration
* authentication
* registration
* login
* JWT protection
* task CRUD routes
* pagination

### models.py

Contains database models such as:

* User
* Task

### schemas.py

Contains Marshmallow schemas used for:

* validation
* input checking
* serialization

### extensions.py

Contains shared Flask extensions such as SQLAlchemy.

### migrations/

Contains database migration files generated by Flask-Migrate/Alembic.

### testing/

Contains automated tests.

### conftest.py

Provides pytest fixtures and test database setup.

---

# 8. Database Design

The application contains two primary entities:

1. User
2. Task

## 8.1 User Entity

A User represents an individual registered with the system.

Typical attributes include:

```text
User
----------------
id
username
email
password_hash
```

The password is not stored as plain text.

Instead, the password is converted into a secure hash using Flask-Bcrypt.

---

# 9. Task Entity

A Task represents a task belonging to a user.

Typical attributes include:

```text
Task
----------------
id
title
description
status
priority
due_date
created_at
user_id
```

The `user_id` is a foreign key that identifies the owner of the task.

---

# 10. User–Task Relationship

The relationship between User and Task is:

```text
One User
   |
   |---- Task 1
   |
   |---- Task 2
   |
   |---- Task 3
   |
   |---- Task N
```

Therefore, the relationship is:

**One-to-Many**

One user can have many tasks, while each task belongs to one user.

The `user_id` field in the Task table establishes ownership.

This relationship is important for authorization because the application can determine whether the currently authenticated user owns a particular task.

---

# 11. User Registration

The API provides:

```text
POST /register
```

A user provides:

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```

The API checks that:

* username exists
* email exists
* password exists
* username/email are not already registered

The password is then hashed using Bcrypt.

The password itself is never stored in the database.

A successful registration returns HTTP status:

```text
201 Created
```

Example response:

```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
}
```

---

# 12. Password Security

Passwords are protected using Flask-Bcrypt.

The application uses:

```python
bcrypt.generate_password_hash(password)
```

During login, the submitted password is checked against the stored hash using:

```python
bcrypt.check_password_hash(
    user.password_hash,
    password
)
```

This is more secure than storing passwords directly.

For example, instead of storing:

```text
password123
```

the database stores a password hash.

Even if someone obtains the database, the original password is not directly available.

---

# 13. User Login

The login endpoint is:

```text
POST /login
```

Example request:

```json
{
    "email": "test@example.com",
    "password": "password123"
}
```

The server:

1. Searches for the user by email.
2. Checks whether the user exists.
3. Compares the supplied password with the stored password hash.
4. Creates a JWT access token if authentication succeeds.

Example response:

```json
{
    "message": "Login successful",
    "access_token": "JWT_TOKEN",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
}
```

---

# 14. JWT Authentication

The application uses JSON Web Tokens for authentication.

JWT allows the server to identify the user making a protected request.

After successful login, the client receives an access token.

The token must be included in protected requests using:

```text
Authorization: Bearer <token>
```

For example:

```text
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

Protected Flask routes use:

```python
@jwt_required()
```

This means the endpoint cannot be accessed without a valid JWT.

---

# 15. Protected Endpoint

The application contains:

```text
GET /protected
```

This route demonstrates JWT authentication.

A valid JWT allows access.

A request without a valid token is rejected.

This demonstrates that authentication is enforced before protected operations are performed.

---

# 16. Authentication Flow

The authentication process can be summarized as:

```text
User
 |
 | POST /register
 v
Create Account
 |
 | POST /login
 v
Verify Credentials
 |
 v
Generate JWT
 |
 v
Return Access Token
 |
 | Authorization: Bearer TOKEN
 v
Protected Endpoint
 |
 v
Verify JWT
 |
 v
Identify User
 |
 v
Perform Operation
```

---

# 17. REST API Endpoints

The API provides the following endpoints:

| Method | Endpoint      | Purpose             | Authentication |
| ------ | ------------- | ------------------- | -------------- |
| GET    | `/`           | API status          | No             |
| POST   | `/register`   | Register user       | No             |
| POST   | `/login`      | Login               | No             |
| GET    | `/protected`  | Test authentication | Yes            |
| GET    | `/tasks`      | Get user's tasks    | Yes            |
| POST   | `/tasks`      | Create task         | Yes            |
| GET    | `/tasks/<id>` | Get one task        | Yes            |
| PATCH  | `/tasks/<id>` | Update task         | Yes            |
| DELETE | `/tasks/<id>` | Delete task         | Yes            |

---

# 18. Home Endpoint

```text
GET /
```

This endpoint confirms that the API is running.

Example response:

```json
{
    "message": "Secure Task API is running"
}
```

Expected HTTP status:

```text
200 OK
```

---

# 19. Create Task

The endpoint is:

```text
POST /tasks
```

Authentication is required.

Example request:

```json
{
    "title": "Study Flask",
    "description": "Complete Flask assignment",
    "status": "pending",
    "priority": "medium"
}
```

The server obtains the authenticated user's ID from the JWT.

The task is then associated with that user.

Example:

```text
Task.user_id = current_user_id
```

Expected status:

```text
201 Created
```

---

# 20. Retrieve Tasks

The endpoint is:

```text
GET /tasks
```

The endpoint is protected by JWT.

Only tasks belonging to the authenticated user are returned.

The application filters tasks using the authenticated user's ID.

Conceptually:

```python
Task.query.filter_by(
    user_id=current_user_id
)
```

This prevents users from automatically seeing all tasks in the database.

---

# 21. Retrieve a Single Task

The endpoint is:

```text
GET /tasks/<id>
```

For example:

```text
GET /tasks/5
```

The application checks both:

```text
task ID
+
current user ID
```

This ensures that the requested task belongs to the authenticated user.

If it does not belong to the user, the API returns:

```text
404 Not Found
```

with a message indicating that the task was not found or access was denied.

---

# 22. Update Task

The endpoint is:

```text
PATCH /tasks/<id>
```

Example:

```json
{
    "title": "Updated task",
    "status": "completed"
}
```

The server:

1. Authenticates the user.
2. Finds the task.
3. Confirms ownership.
4. Validates the submitted data.
5. Updates only the supplied fields.
6. Saves the changes.

Expected status:

```text
200 OK
```

---

# 23. Delete Task

The endpoint is:

```text
DELETE /tasks/<id>
```

The server verifies:

1. JWT authentication.
2. Task existence.
3. Task ownership.

If successful, the task is deleted.

Expected status:

```text
200 OK
```

Example:

```json
{
    "message": "Task deleted successfully"
}
```

---

# 24. Authorization and Ownership

Authentication and authorization are different concepts.

## Authentication

Authentication answers:

> Who are you?

JWT is used for authentication.

## Authorization

Authorization answers:

> Are you allowed to perform this operation?

The application implements ownership-based authorization.

For example:

```text
Amina
 |
 +---- Task 1
 |
 +---- Task 2

Brian
 |
 +---- Task 3
```

Amina should not be able to modify Brian's Task 3.

Brian should not be able to delete Amina's Task 1.

The API checks:

```text
task.user_id == current_user_id
```

before allowing access.

---

# 25. Ownership Security Example

Suppose Amina creates:

```text
Task ID = 10
User ID = 1
```

Brian logs in and receives:

```text
User ID = 2
```

If Brian requests:

```text
GET /tasks/10
```

the API effectively searches for:

```text
Task ID = 10
AND
User ID = 2
```

Because Task 10 belongs to User 1, no matching record is found.

Therefore, Brian cannot access the task.

This prevents insecure direct object access.

---

# 26. Marshmallow Validation

Marshmallow is used to validate incoming task data.

Validation helps ensure that clients cannot submit invalid information.

Examples of data that should be validated include:

* title
* status
* priority
* due date

---

# 27. Task Validation

A valid task could be:

```json
{
    "title": "Complete assignment",
    "description": "Finish Flask project",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-09-30"
}
```

Invalid input should be rejected rather than stored in the database.

---

# 28. Required Title Validation

A task must have a title.

For example:

```json
{
    "description": "No title supplied"
}
```

should result in a validation error.

Expected response:

```text
400 Bad Request
```

This prevents incomplete task records.

---

# 29. Status Validation

The task status should only accept valid values defined by the application's schema.

For example:

```text
pending
in_progress
completed
```

An invalid value such as:

```json
{
    "status": "random_status"
}
```

should be rejected.

Expected response:

```text
400 Bad Request
```

---

# 30. Priority Validation

Priority should similarly be restricted to valid values.

Typical values include:

```text
low
medium
high
```

An invalid priority should result in:

```text
400 Bad Request
```

---

# 31. Date Validation

The API uses the date format:

```text
YYYY-MM-DD
```

Example:

```text
2026-09-30
```

An invalid date should be rejected.

Date validation prevents malformed dates from being stored in the database.

---

# 32. Pagination

The `/tasks` endpoint supports pagination.

Pagination is important when a user has many tasks.

Instead of returning thousands of records in a single response, the API divides the results into pages.

The default page size is:

```text
5 tasks
```

The API accepts:

```text
?page=1&per_page=5
```

Example:

```text
GET /tasks?page=2&per_page=5
```

---

# 33. Pagination Example

Suppose a user has 15 tasks.

With:

```text
per_page = 5
```

the results become:

```text
Page 1 → Tasks 1–5
Page 2 → Tasks 6–10
Page 3 → Tasks 11–15
```

The response includes pagination metadata.

Example:

```json
{
    "tasks": [],
    "page": 1,
    "per_page": 5,
    "total": 15,
    "pages": 3
}
```

---

# 34. Pagination Calculation

The application determines the starting record using:

```python
start = (page - 1) * per_page
```

For page 1:

```text
start = (1 - 1) × 5
      = 0
```

For page 2:

```text
start = (2 - 1) × 5
      = 5
```

For page 3:

```text
start = (3 - 1) × 5
      = 10
```

This allows the API to return the appropriate records.

---

# 35. Database Migrations

The project uses Flask-Migrate for database schema management.

Migrations allow changes to database models to be tracked and applied systematically.

Typical commands include:

```bash
flask db init
```

to initialize migrations.

```bash
flask db migrate -m "Initial migration"
```

to generate a migration.

```bash
flask db upgrade
```

to apply the migration.

---

# 36. Why Database Migrations Are Important

Without migrations, developers may have to manually modify database tables whenever models change.

Migrations provide:

* version control for database structure
* repeatability
* safer schema changes
* collaboration between developers
* rollback/version management

They are particularly important in team projects.

---

# 37. Automated Testing

The project uses **pytest** for automated testing.

Tests are located under:

```text
testing/
```

The test structure includes:

```text
testing/
├── conftest.py
├── test_auth.py
└── test_tasks.py
```

---

# 38. Test Fixture

`conftest.py` provides the Flask test client.

The test environment uses an isolated SQLite database.

This means tests do not need to depend on the production database.

The fixture creates database tables before a test and cleans them up afterward.

This makes tests repeatable.

---

# 39. Authentication Tests

The authentication tests verify:

### Home endpoint

```text
GET /
```

Expected:

```text
200 OK
```

### Registration

```text
POST /register
```

Expected:

```text
201 Created
```

### Login

```text
POST /login
```

Correct credentials should return:

```text
200 OK
```

### Invalid login

Incorrect password should return:

```text
401 Unauthorized
```

---

# 40. Protected Route Tests

The project tests that unauthenticated users cannot access protected endpoints.

For example:

```text
GET /tasks
```

without a JWT should return:

```text
401 Unauthorized
```

or the appropriate authentication error.

Similarly:

```text
POST /tasks
```

without authentication should fail.

This verifies that `@jwt_required()` is functioning correctly.

---

# 41. CRUD Tests

The test suite covers the main task operations.

## Create

```text
POST /tasks
```

Expected:

```text
201 Created
```

## Read

```text
GET /tasks
```

Expected:

```text
200 OK
```

## Update

```text
PATCH /tasks/<id>
```

Expected:

```text
200 OK
```

## Delete

```text
DELETE /tasks/<id>
```

Expected:

```text
200 OK
```

---

# 42. Authorization Tests

The test suite creates two users:

```text
Amina
Brian
```

Amina creates a task.

Brian attempts to access the task.

The API must reject Brian.

This verifies ownership authorization.

The same principle should be applied to:

* GET
* PATCH
* DELETE

so that another user cannot read, modify, or delete someone else's task.

---

# 43. Pagination Tests

Pagination testing verifies that:

* 15 tasks can be created.
* Page 1 returns 5 tasks.
* Page 2 returns 5 tasks.
* Page 3 returns 5 tasks.
* `total` is 15.
* `pages` is 3.

This confirms that the pagination implementation works correctly.

---

# 44. Validation Tests

Validation tests should verify:

| Test             | Expected |
| ---------------- | -------- |
| Valid task       | Success  |
| Missing title    | 400      |
| Invalid status   | 400      |
| Invalid priority | 400      |
| Invalid date     | 400      |

Testing invalid data is important because a secure API must not only handle valid requests; it must also reject invalid requests correctly.

---

# 45. Test Command

The complete test suite can be executed using:

```bash
python -m pytest -v
```

The `-v` option provides verbose test results.

Example successful output:

```text
============================= test session starts =============================
...
PASSED testing/test_auth.py
PASSED testing/test_tasks.py
...
============================== XX passed ======================================
```

During development, the project successfully progressed to:

```text
11 passed
```

for the implemented authentication and task tests before the additional pagination and validation test expansion.

---

# 46. Why `python -m pytest` Is Used

The project uses a Python virtual environment.

Therefore:

```bash
python -m pytest -v
```

ensures that pytest is executed using the same Python interpreter as the active virtual environment.

This avoids problems where:

```bash
pytest
```

may point to a different Python installation.

---

# 47. Error Handling

The API uses HTTP status codes to communicate the result of operations.

Common status codes include:

| Status | Meaning                                      |
| ------ | -------------------------------------------- |
| 200    | Successful request                           |
| 201    | Resource successfully created                |
| 400    | Bad request/validation error                 |
| 401    | Authentication required/invalid credentials  |
| 404    | Resource not found or unauthorized ownership |
| 409    | Conflict, such as duplicate username/email   |

Using standard HTTP status codes makes the API easier for frontend developers and other clients to consume.

---

# 48. Security Features

The project implements several security measures.

## 48.1 Password hashing

Passwords are hashed using Bcrypt.

## 48.2 JWT authentication

Protected endpoints require a valid access token.

## 48.3 Ownership authorization

Users can only access their own tasks.

## 48.4 Input validation

Invalid task data is rejected.

## 48.5 Protected CRUD operations

Task creation, retrieval, modification and deletion require authentication.

## 48.6 Database isolation during tests

Testing uses a separate test database environment.

---

# 49. Environment Configuration

The application contains configuration values such as:

```python
app.config["SQLALCHEMY_DATABASE_URI"]
app.config["JWT_SECRET_KEY"]
```

For a production deployment, sensitive values such as the JWT secret should not be hard-coded.

They should instead be stored in environment variables.

For example:

```text
DATABASE_URL
JWT_SECRET_KEY
```

A `.env` file can be used during development, provided that it is excluded from Git.

---

# 50. Installation

## Step 1: Clone the repository

```bash
git clone <repository-url>
```

Navigate into the project:

```bash
cd Full-Auth-Flask-Backend--Productivity-App
```

## Step 2: Create virtual environment

```bash
python3 -m venv venv
```

## Step 3: Activate virtual environment

Linux/WSL:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

---

# 51. Database Setup

Initialize the migration system:

```bash
flask db init
```

Generate migration:

```bash
flask db migrate -m "Initial database migration"
```

Apply migration:

```bash
flask db upgrade
```

---

# 52. Running the Application

Run:

```bash
python app.py
```

The Flask development server will start.

The API can then be accessed through the local server address.

The root endpoint can be tested using:

```text
GET /
```

Expected response:

```json
{
    "message": "Secure Task API is running"
}
```

---

# 53. Testing with Postman

The API can be tested using Postman.

## Registration

Method:

```text
POST
```

URL:

```text
/register
```

Body:

```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```

---

## Login

Method:

```text
POST
```

URL:

```text
/login
```

Body:

```json
{
    "email": "test@example.com",
    "password": "password123"
}
```

Copy the returned:

```text
access_token
```

---

## Create Task

Method:

```text
POST
```

URL:

```text
/tasks
```

Header:

```text
Authorization: Bearer <access_token>
```

Body:

```json
{
    "title": "Complete project",
    "description": "Finish Flask API",
    "status": "pending",
    "priority": "high"
}
```

---

# 54. Git and GitHub Workflow

Git was used for version control and team collaboration.

The development process involved feature branches.

Examples include:

```text
feature/project-setup
feature/authentication
feature/task-crud
feature/testing-documentation
```

Each team member could work independently before changes were merged into the main project.

---

# 55. Feature Branch Strategy

A typical workflow was:

```text
main
 |
 +--- feature/project-setup
 |
 +--- feature/authentication
 |
 +--- feature/task-crud
 |
 +--- feature/testing-documentation
```

After development and testing, feature branches were merged into the main branch.

This reduced the risk of developers directly interfering with each other's work.

---

# 56. Person 6 Responsibilities

The Person 6 role focused on:

1. Testing
2. Integration
3. Bug fixing
4. Documentation
5. Authentication test coverage
6. CRUD test coverage
7. Authorization testing
8. Pagination testing
9. Validation testing
10. Final integration verification

The testing/documentation branch was:

```text
feature/testing-documentation
```

---

# 57. Integration Process

Integration involved checking that the components developed by different team members worked together.

The main integration areas were:

```text
User Model
     |
     v
Authentication
     |
     v
JWT
     |
     v
Task Model
     |
     v
CRUD
     |
     v
Marshmallow Validation
     |
     v
Pagination
     |
     v
Testing
```

The final application had to ensure that all components could communicate correctly.

---

# 58. Common Integration Issue Encountered

One important integration issue involved endpoint naming.

The testing code initially used:

```text
/signup
```

while the actual application route was:

```text
/register
```

This resulted in:

```text
404 Not Found
```

The tests were corrected to use:

```text
/register
```

This demonstrates why integration testing is important: different team members may implement or assume different endpoint names.

---

# 59. JWT Integration Issue

Another testing issue occurred when the task test successfully logged in but did not include the JWT token in the subsequent request.

For example, simply logging in does not automatically authenticate another request in JWT-based APIs.

The token must be extracted:

```python
token = login_response.get_json()["access_token"]
```

and included:

```python
headers={
    "Authorization": f"Bearer {token}"
}
```

This was necessary for protected `/tasks` endpoints.

---

# 60. Testing Strategy

The testing strategy follows several levels.

### Level 1 – Public endpoints

Test:

```text
GET /
POST /register
POST /login
```

### Level 2 – Authentication

Test:

```text
Correct credentials
Incorrect password
Missing token
Invalid token
```

### Level 3 – CRUD

Test:

```text
Create
Read
Update
Delete
```

### Level 4 – Authorization

Test:

```text
Owner access
Non-owner access
```

### Level 5 – Validation

Test:

```text
Valid data
Invalid data
```

### Level 6 – Pagination

Test:

```text
Page 1
Page 2
Page 3
```

---

# 61. Functional Requirements

The system should allow a registered user to:

* register an account
* log in
* receive an authentication token
* create tasks
* view their tasks
* view an individual task
* update their tasks
* delete their tasks
* paginate task results

The system should prevent:

* unauthenticated task access
* invalid login
* access to another user's tasks
* invalid task data

---

# 62. Non-Functional Requirements

The system should provide:

### Security

Passwords must be hashed and protected routes must require authentication.

### Reliability

The application should return appropriate errors rather than crashing.

### Maintainability

The application should have organized models, routes, schemas, tests and documentation.

### Scalability

Pagination should prevent unnecessarily large responses.

### Testability

Automated tests should verify the application's functionality.

### Collaboration

Git and GitHub should support team development.

---

# 63. Advantages of the System

The system provides:

* secure authentication
* password hashing
* JWT authorization
* ownership protection
* RESTful endpoints
* structured database models
* validation
* pagination
* automated testing
* migration support
* collaborative development

---

# 64. Limitations

The current development implementation uses SQLite, which is suitable for development and testing but may not be ideal for a large production deployment.

The API would require additional production hardening such as:

* environment-based secrets
* HTTPS
* refresh tokens
* rate limiting
* stronger logging
* centralized error handling
* production database such as PostgreSQL
* deployment configuration
* CORS configuration where required

---

# 65. Future Improvements

Possible future improvements include:

1. PostgreSQL production database.
2. Refresh token implementation.
3. Password reset functionality.
4. Email verification.
5. User profile management.
6. Advanced task searching.
7. Task filtering.
8. Task sorting.
9. Role-based access control.
10. Rate limiting.
11. API documentation using Swagger/OpenAPI.
12. Docker deployment.
13. Continuous Integration using GitHub Actions.
14. Production deployment using a cloud platform.
15. More comprehensive automated tests.

---

# 66. Example API Workflow

A complete user workflow is:

```text
1. Register
       |
       v
2. Login
       |
       v
3. Receive JWT
       |
       v
4. Send JWT with task request
       |
       v
5. Create Task
       |
       v
6. Retrieve Tasks
       |
       v
7. Update Task
       |
       v
8. Delete Task
```

---

# 67. Security Workflow

The security process is:

```text
Client
  |
  | Credentials
  v
/login
  |
  | Verify password hash
  v
JWT generated
  |
  | Bearer Token
  v
Protected endpoint
  |
  v
JWT verification
  |
  v
Get current user ID
  |
  v
Check task ownership
  |
  v
Allow/Deny operation
```

---

# 68. Examination/Viva Questions and Answers

## Question 1: Why did you use Flask?

**Answer:**

Flask is a lightweight Python web framework that provides the flexibility needed to build REST APIs. It is easy to integrate with SQLAlchemy, JWT authentication, Bcrypt and Marshmallow.

---

## Question 2: What is REST?

**Answer:**

REST stands for Representational State Transfer. It is an architectural style for building web services using standard HTTP methods such as GET, POST, PATCH and DELETE.

---

## Question 3: What is CRUD?

**Answer:**

CRUD stands for:

```text
C – Create
R – Read
U – Update
D – Delete
```

In this project, CRUD operations are applied to tasks.

---

## Question 4: Why is JWT used?

**Answer:**

JWT is used to authenticate users and protect private endpoints. After login, the server issues a token that the client sends with subsequent protected requests.

---

## Question 5: What is the difference between authentication and authorization?

**Answer:**

Authentication determines who the user is. Authorization determines what that authenticated user is allowed to access or modify.

---

## Question 6: Why is Bcrypt used?

**Answer:**

Bcrypt is used to securely hash passwords before they are stored in the database. The original password is therefore not stored directly.

---

## Question 7: Why should passwords not be stored as plain text?

**Answer:**

If the database is compromised, plain-text passwords would immediately be exposed. Password hashing provides an additional security layer.

---

## Question 8: Why do you need `@jwt_required()`?

**Answer:**

It protects an endpoint by requiring the request to contain a valid JWT.

---

## Question 9: How do you prevent one user from accessing another user's task?

**Answer:**

The API obtains the authenticated user's ID from the JWT and queries the task using both the task ID and the user's ID.

For example:

```python
Task.query.filter_by(
    id=id,
    user_id=current_user_id
).first()
```

---

## Question 10: Why do you use pagination?

**Answer:**

Pagination prevents the API from returning a very large number of records in one response. It improves performance and reduces the amount of data transferred.

---

## Question 11: Why is Marshmallow used?

**Answer:**

Marshmallow is used to validate and serialize data. It helps ensure that incoming task data conforms to the expected structure and values.

---

## Question 12: What is SQLAlchemy?

**Answer:**

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper. It allows developers to work with database tables through Python models and queries.

---

## Question 13: What is a migration?

**Answer:**

A migration records changes to the database schema so that database structures can be updated consistently across development environments.

---

## Question 14: Why use pytest?

**Answer:**

Pytest provides a simple and powerful framework for automated testing. It allows us to verify that application functionality continues to work after changes.

---

## Question 15: What is a fixture?

**Answer:**

A pytest fixture provides reusable test setup and resources. In this project, the fixture creates a test client and prepares an isolated database for tests.

---

## Question 16: What does HTTP 401 mean?

**Answer:**

HTTP 401 means that authentication is required or the supplied authentication credentials are invalid.

---

## Question 17: What does HTTP 404 mean?

**Answer:**

HTTP 404 means that the requested resource could not be found. In this application, it is also used when a user attempts to access a task that does not belong to them.

---

## Question 18: Why use HTTP 201 for task creation?

**Answer:**

HTTP 201 Created indicates that a new resource has successfully been created.

---

## Question 19: Why use PATCH instead of PUT?

**Answer:**

PATCH is appropriate when updating only selected fields of an existing resource. In this application, a user can update individual task fields without replacing the entire task.

---

## Question 20: What happens if the JWT is missing?

**Answer:**

The protected endpoint rejects the request because the `@jwt_required()` decorator requires a valid JWT.

---

# 69. Demonstration Sequence for Examination

During a practical examination, demonstrate the system in this order:

### Step 1 – Start the application

```bash
python app.py
```

### Step 2 – Show the home endpoint

```text
GET /
```

### Step 3 – Register a user

```text
POST /register
```

### Step 4 – Login

```text
POST /login
```

Show the returned JWT.

### Step 5 – Attempt unauthorized access

Call:

```text
GET /tasks
```

without a token.

Show that the request is rejected.

### Step 6 – Add JWT

Use:

```text
Authorization: Bearer <token>
```

### Step 7 – Create a task

```text
POST /tasks
```

### Step 8 – Retrieve tasks

```text
GET /tasks
```

### Step 9 – Update the task

```text
PATCH /tasks/<id>
```

### Step 10 – Delete the task

```text
DELETE /tasks/<id>
```

### Step 11 – Demonstrate authorization

Create Amina and Brian.

Show that Brian cannot access Amina's task.

### Step 12 – Demonstrate pagination

Create 15 tasks.

Show:

```text
?page=1&per_page=5
?page=2&per_page=5
?page=3&per_page=5
```

### Step 13 – Run automated tests

```bash
python -m pytest -v
```

---

# 70. Final Project Checklist

Before submission, verify:

* [x] Flask application created
* [x] User model implemented
* [x] Task model implemented
* [x] User-task relationship implemented
* [x] User registration implemented
* [x] Login implemented
* [x] Bcrypt password hashing implemented
* [x] JWT authentication implemented
* [x] Protected endpoints implemented
* [x] Task creation implemented
* [x] Task retrieval implemented
* [x] Task update implemented
* [x] Task deletion implemented
* [x] Ownership authorization implemented
* [x] Marshmallow validation integrated
* [x] Pagination implemented
* [x] Flask-Migrate configured
* [x] Automated tests created
* [x] Authentication tests implemented
* [x] CRUD tests implemented
* [x] Authorization tests implemented
* [ ] Pagination tests fully implemented
* [ ] Validation tests fully implemented
* [x] README/documentation prepared
* [x] Git/GitHub collaboration used

---

# 71. Conclusion

The Secure Flask REST API Backend – Task Management System demonstrates the development of a secure, structured and testable RESTful backend application.

The project combines Flask, SQLAlchemy, Marshmallow, Bcrypt, JWT and pytest to provide a complete backend solution.

The most important security feature is the combination of JWT authentication and task ownership authorization. Authentication identifies the current user, while authorization ensures that the user can only access resources belonging to them.

The project also demonstrates professional software development practices through database migrations, automated testing, Git branching, collaborative integration and technical documentation.

The resulting API provides a strong foundation for a production task-management application and can be extended with features such as PostgreSQL, refresh tokens, role-based access control, API documentation, rate limiting, CI/CD and cloud deployment.

---

# 72. Summary of Group Responsibilities

| Person   | Responsibility                                     |
| -------- | -------------------------------------------------- |
| Person 1 | Project setup and User model                       |
| Person 2 | Authentication and password security               |
| Person 3 | Task model, relationships and database seed        |
| Person 4 | CRUD endpoints and ownership authorization         |
| Person 5 | Marshmallow validation and pagination              |
| Person 6 | Testing, integration, bug fixing and documentation |

---

# 73. Final Statement

The project successfully demonstrates the complete lifecycle of developing a secure REST API: from database modelling and authentication to CRUD operations, authorization, validation, pagination, testing, integration and documentation.

The implementation also demonstrates collaborative software development through Git/GitHub, feature branches and integration of independently developed components.

The testing and documentation phase provides evidence that the individual components can operate together as one functional backend system.
