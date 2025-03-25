import json
import pytest
from dotenv import load_dotenv
import os
import requests
from data import users
from sqlmodel import Session, select
from app.database.engine import engine
from app.models.models import UserData


load_dotenv()
@pytest.fixture(scope='session')
def base_url():
    base_url = os.getenv('BASE_URL')
    return base_url

@pytest.fixture(scope='module', autouse=False)
def clear_database():
    with Session(engine) as session:
        statement = select(UserData)
        users = session.exec(statement).all()
        for user in users:
            session.delete(user)
        session.commit()

@pytest.fixture(scope='module')
def fill_test_data(base_url, clear_database):
    clear_database
    api_users = {}
    for user in users:
        response = requests.post(f'{base_url}/users', json=users[user])
        api_users[response.json()['id']] = response.json()

    yield api_users

    for user_id in api_users.keys():
        response = requests.delete(f'{base_url}/users/{user_id}')