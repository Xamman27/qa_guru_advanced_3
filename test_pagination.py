import requests
import pytest
from data import users
import math


users_count = len(users)

def test_pagination_get_users_default(base_url):
    response = requests.get(f'{base_url}/users')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == users_count
    assert type(data['items']) == list
    assert data['total'] == users_count
    assert data['page'] == 1
    assert data['size'] == 50
    assert data['pages'] == math.ceil(users_count / 50)


def test_pagination_get_users_size_5(base_url):
    response = requests.get(f'{base_url}/users?size=5')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 5
    assert type(data['items']) == list
    assert data['total'] == users_count
    assert data['page'] == 1
    assert data['size'] == 5
    assert data['pages'] == math.ceil(users_count / 5)


def test_pagination_get_users_size_2(base_url):
    response = requests.get(f'{base_url}/users?size=2')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 2
    assert type(data['items']) == list
    assert data['total'] == users_count
    assert data['page'] == 1
    assert data['size'] == 2
    assert data['pages'] == math.ceil(users_count / 2)


def test_pagination_get_users_page_2_size_5(base_url):
    response = requests.get(f'{base_url}/users?page=2&size=5')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 5
    assert type(data['items']) == list
    assert data['total'] == users_count
    assert data['page'] == 2
    assert data['size'] == 5
    assert data['pages'] == math.ceil(users_count / 5)

def test_pagination_get_users_invalid_page(base_url):
    response = requests.get(f'{base_url}/users?page=9999&size=5')
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 0
    assert type(data['items']) == list
    assert data['total'] == users_count
    assert data['page'] == 9999
    assert data['size'] == 5
    assert data['pages'] == math.ceil(users_count / 5)


def test_pagination_get_users_no_duplicates(base_url):
    all_users = []
    page = 1
    size = 5

    while True:
        response = requests.get(f"{base_url}/users?page={page}&size={size}")
        assert response.status_code == 200
        data = response.json()
        all_users.extend(data['items'])

        if len(data['items']) < size:
            break

        page += 1

    user_ids = [user['id'] for user in all_users]
    assert len(user_ids) == len(set(user_ids))


def test_pagination_get_users_different_pages(base_url):
    size = 5
    page_1_response = requests.get(f'{base_url}/users?page=1&size={size}')
    page_2_response = requests.get(f'{base_url}/users?page=2&size={size}')

    assert page_1_response.status_code == 200
    assert page_2_response.status_code == 200

    page_1 = page_1_response.json()['items']
    page_2 = page_2_response.json()['items']

    assert page_1 == list(users.values())[:size]
    assert page_2 == list(users.values())[size:size * 2]

