import requests
import random
import string
import pytest
from response_definitions import SuccessResponses
from test_data import URLS



@pytest.fixture
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(URLS['courier'], json=payload)

    if response.status_code == 201:
        login_pass.extend([login, password, first_name])

    return login_pass


@pytest.fixture
def delete_courier():
    def _delete_courier(courier_id):
        response_delete = requests.delete(f'{URLS["courier"]}/{courier_id}')

    return _delete_courier


@pytest.fixture
def get_id_courier():
    def _get_id_courier(credentials):
        payload = {
            "login": credentials['login'],
            "password": credentials['password']
        }
        login_response = requests.post(URLS['login'], json={
            "login": payload['login'], "password": payload['password']})
        response_data = login_response.json()
        id_courier = response_data["id"]
        return id_courier

    return _get_id_courier
