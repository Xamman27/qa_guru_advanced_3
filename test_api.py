import requests
import pytest
import random

#STATUS
def test_service_status(base_url):
    response = requests.get(f'{base_url}/status')
    assert response.json()['database']

def test_clear_database(base_url, clear_database):
    response = requests.get(f"{base_url}/users")
    assert len(response.json()['items']) == 0

#GET
def test_get_user_by_id(base_url, fill_test_data):
    test_user = random.choice(list(fill_test_data.values()))
    url = f"{base_url}/users/{test_user['id']}"
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        body = response.json()
        data = body['data']
        assert data['email'] == test_user['email'], f"Expected email {test_user['email']}, but got {data['email']}"
        assert data['id'] == test_user['id'], f"Expected id {test_user}, but got {data['id']}"
    except requests.exceptions.HTTPError as http_err:
        pytest.fail(f"HTTP error occurred: {http_err}")
    except Exception as err:
        pytest.fail(f"Other error occurred: {err}")

def test_get_user_list(base_url, fill_test_data):
    response = requests.get(f"{base_url}/users")
    api_users_list = response.json()['items']
    assert len(api_users_list) == len(fill_test_data)

def test_get_user_list_no_duplicates(base_url):
    response = requests.get(f"{base_url}/users")
    api_users_list = response.json()['items']
    seen_ids = set()
    for user in api_users_list:
        user_id = user['id']
        assert user_id not in seen_ids
        seen_ids.add(user_id)

#POST
def test_post_create_users_test_response_data(base_url):
    body = {
        "email": "test_email",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "test_avatar"
    }
    response = requests.post(url=f"{base_url}/users", json=body)
    assert response.status_code == 200
    new_user = response.json()
    values_equal = all(new_user[key] == body[key] for key in new_user if key in body)
    assert values_equal
    response = requests.delete(f"{base_url}/users/{new_user['id']}")
    assert response.status_code == 200

def test_get_user_after_create_user(base_url):
    body = {
        "email": "test_email",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "test_avatar"
    }
    response = requests.post(url=f"{base_url}/users", json=body)
    assert response.status_code == 200
    new_user = response.json()
    response = requests.get(f"{base_url}/users/{new_user['id']}")
    api_user = response.json()['data']
    values_equal = all(new_user[key] == api_user[key] for key in new_user if key in api_user)
    assert values_equal
    response = requests.delete(f"{base_url}/users/{new_user['id']}")
    assert response.status_code == 200

def test_get_user_list_after_create_user(base_url, fill_test_data):
    body = {
        "email": "test_email",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "test_avatar"
    }
    response = requests.post(url=f"{base_url}/users", json=body)
    assert response.status_code == 200
    new_user = response.json()
    fill_test_data[new_user['id']] = new_user

    response = requests.get(f"{base_url}/users")
    api_user_list = response.json()['items']

    values_equal = all(fill_test_data[key] == api_user_list[key] for key in fill_test_data if key in api_user_list)
    assert values_equal
    assert len(api_user_list) == len(fill_test_data)


def test_patch_update_all_data(base_url):
    body = {
        "email": "test_email",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "test_avatar"
    }
    response = requests.post(url=f"{base_url}/users", json=body)
    assert response.status_code == 200
    new_user = response.json()
    print(new_user)
    new_body = {
        "first_name": "1",
        "last_name": "1",
        "avatar": "1"
    }
    response = requests.patch(url=f"{base_url}/users/{new_user['id']}", json=new_body)
    api_new_user = response.json()
    value_equal = all(new_body[key] == api_new_user[key] for key in new_body if key in api_new_user)
    assert value_equal
