from datetime import date, timedelta

from app import app
from extensions import db
from models import User, Task

with app.app_context():
    # Start clean each time this script runs
    db.drop_all()
    db.create_all()

    # --- Users ---
    amina = User(
        username="amina",
        email="amina@example.com",
        password_hash="placeholder-will-be-hashed-by-auth-flow"
    )
    brian = User(
        username="brian",
        email="brian@example.com",
        password_hash="placeholder-will-be-hashed-by-auth-flow"
    )

    db.session.add_all([amina, brian])
    db.session.commit()  # commit here so amina.id / brian.id are assigned

    # --- Tasks: 10 for Amina, 5 for Brian (15 total, enough for pagination testing) ---
    statuses = ["pending", "in_progress", "completed"]
    priorities = ["low", "medium", "high"]

    tasks = []
    for i in range(1, 11):
        tasks.append(Task(
            title=f"Amina Task {i}",
            description=f"Sample task {i} for Amina",
            status=statuses[i % 3],
            priority=priorities[i % 3],
            due_date=date.today() + timedelta(days=i),
            user_id=amina.id
        ))

    for i in range(1, 6):
        tasks.append(Task(
            title=f"Brian Task {i}",
            description=f"Sample task {i} for Brian",
            status=statuses[i % 3],
            priority=priorities[i % 3],
            due_date=date.today() + timedelta(days=i),
            user_id=brian.id
        ))

    db.session.add_all(tasks)
    db.session.commit()

    print(f"Seeded {User.query.count()} users and {Task.query.count()} tasks.")