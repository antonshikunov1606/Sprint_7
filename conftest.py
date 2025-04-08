import requests
import random
import string
import pytest
from tests.response_definitions import SuccessResponses, ErrorResponses

URL_HOME = 'https://qa-scooter.praktikum-services.ru/'


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

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)

    if response.status_code == 201:
        login_pass.extend([login, password, first_name])

    return login_pass


@pytest.fixture
def delete_courier():
    def _delete_courier(courier_id):
        response_delete = requests.delete(f'{URL_HOME}/api/v1/courier/{courier_id}')
        response_delete_data = response_delete.json()
        expected_response_data = SuccessResponses.SUCCESSFUL_DELETE_USER

        assert response_delete.status_code == 200, f'Ожидаем код 200, но получили {response_delete.status_code}'
        assert response_delete_data == expected_response_data, \
            f"Ожидаем ответ: {expected_response_data}, но получили: {response_delete_data}"

    return _delete_courier


@pytest.fixture
def get_id_courier():
    def _get_id_courier(credentials):
        payload = {
            "login": credentials['login'],
            "password": credentials['password']
        }
        login_response = requests.post(f"{URL_HOME}/api/v1/courier/login", json={
            "login": payload['login'], "password": payload['password']})
        response_data = login_response.json()
        id_courier = response_data["id"]
        expected_response_data = SuccessResponses.success_login(id_courier)
        assert login_response.status_code == 200, f'Ожидаем код 200, но получили {login_response.status_code}'
        assert response_data == expected_response_data, \
            f"Ожидаем ответ: {expected_response_data}, но получили: {response_data}"
        return id_courier

    return _get_id_courier
