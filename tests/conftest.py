import pytest
from app import create_app, db
from sqlalchemy import create_engine, text

TEST_DB_NAME = "rotaguard_test"
TEST_DB_URL = f"postgresql://rotaguard:rotapassword@db:5432/{TEST_DB_NAME}"
ADMIN_DB_URL = "postgresql://rotaguard:rotapassword@db:5432/postgres"

import subprocess
import os
def reset_test_db():
    engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME} OWNER rotaguard"))
    # Run migrations on the new test DB
    env = os.environ.copy()
    env["DATABASE_URL"] = TEST_DB_URL
    subprocess.run(["flask", "db", "upgrade"], check=True, env=env)

@pytest.fixture(scope="session", autouse=True)
def _test_db():
    reset_test_db()

@pytest.fixture
def client():
    app = create_app(database_uri=TEST_DB_URL)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.session.remove()
        db.drop_all()

