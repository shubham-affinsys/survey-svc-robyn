# conftest.py
import pytest
from robyn import Robyn, Request, Response
from src.models import SessionLocal, Base, engine
from robyn import Response

from src.__main__ import app
@pytest.fixture(scope="function")
def test_client():

    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as session:
        yield session
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_robyn():
    
    yield app