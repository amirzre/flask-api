import pytest
from sqlalchemy.orm import scoped_session, sessionmaker

from src.config import config
from src.extensions import db
from src.server import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_TEST_URL
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def engine(app):
    return db.engine


@pytest.fixture(scope="session")
def _db(engine, app):
    db.metadata.create_all(bind=engine)
    yield db
    db.session.remove()
    db.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def session(_db, engine):
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    db_session = scoped_session(session_factory)

    _db.session = db_session
    yield db_session

    transaction.rollback()
    connection.close()
    db_session.remove()


@pytest.fixture
def client(app, session):
    return app.test_client()
