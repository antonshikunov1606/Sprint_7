import allure
import pytest
import requests
from faker import Faker
import string
from response_definitions import SuccessResponses, ErrorResponses

URL_HOME = 'https://qa-scooter.praktikum-services.ru/'


class TestLoginCourier:
    @allure.title("Проверка авторизации курьера")
    def test_successful_login_courier(self, register_new_courier_and_return_login_password, delete_courier):
        credentials = register_new_courier_and_return_login_password
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }

        with allure.step("Проверка успешной авторизации курьера"):
            login_response = requests.post(f"{URL_HOME}/api/v1/courier/login", json={
                "login": payload['login'], "password": payload['password']})
            response_data = login_response.json()
            id_courier = response_data["id"]
            expected_response_data = SuccessResponses.success_login(id_courier)
            assert login_response.status_code == 200, f'Ожидаем код 200, но получили {login_response.status_code}'
            assert response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}, но получили: {response_data}"

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности авторизации курьера без логина")
    def test_login_courier_without_login_not_allowed(
            self, register_new_courier_and_return_login_password, get_id_courier, delete_courier
    ):
        credentials = register_new_courier_and_return_login_password
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }
        with allure.step("Проверка ошибка авторизации курьера без логина"):
            login_response = requests.post(f"{URL_HOME}/api/v1/courier/login", json={
                "password": payload['password']
            })
            login_response_data = login_response.json()
            expected_response_data = ErrorResponses.INSUFFICIENT_DATA_FOR_LOGIN
            assert login_response.status_code == 400, f'Ожидаем код 400, а получили {login_response.status_code}'
            assert login_response_data == expected_response_data, \
                f'Ожидаем ответ: {expected_response_data}, но получили: {login_response_data}'

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности авторизации курьера без пароля")
    def test_login_courier_without_password_not_allowed(
            self, register_new_courier_and_return_login_password, get_id_courier, delete_courier
    ):
        credentials = register_new_courier_and_return_login_password
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }
        with allure.step("Проверка ошибка авторизации курьера без пароля"):
            login_response = requests.post(f"{URL_HOME}/api/v1/courier/login", json={
                "login": payload['login']
            })
            login_response_data = login_response.json()
            expected_response_data = ErrorResponses.INSUFFICIENT_DATA_FOR_LOGIN
            assert login_response.status_code == 400, f'Ожидаем код 400, а получили {login_response.status_code}'
            assert login_response_data == expected_response_data, \
                f'Ожидаем ответ: {expected_response_data}, но получили: {login_response_data}'

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности авторизации курьера с неправильным логином")
    def test_login_courier_with_incorrect_login_not_allowed(
            self, register_new_courier_and_return_login_password, get_id_courier, delete_courier
    ):
        credentials = register_new_courier_and_return_login_password
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }
        fake = Faker()
        #  генерируем рандомный логин из 15-ти символов
        random_login = ''.join(fake.random_choices(elements=string.ascii_letters, length=15))

        with allure.step("Проверка ошибка авторизации курьера с неправильным логином"):
            login_response = requests.post(f"{URL_HOME}/api/v1/courier/login", json={
                "login": random_login, "password": payload['login']
            })
            login_response_data = login_response.json()
            expected_response_data = ErrorResponses.NON_EXISTENT_DATA_FOR_LOGIN
            assert login_response.status_code == 404, f'Ожидаем код 404, а получили {login_response.status_code}'
            assert login_response_data == expected_response_data, \
                f'Ожидаем ответ: {expected_response_data}, но получили: {login_response_data}'

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности авторизации курьера с неправильным паролем")
    def test_login_courier_with_incorrect_password_not_allowed(
            self, register_new_courier_and_return_login_password, get_id_courier, delete_courier
    ):
        credentials = register_new_courier_and_return_login_password
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }
        fake = Faker()
        #  генерируем рандомный пароль из 15-ти символов
        random_password = ''.join(fake.random_choices(elements=string.ascii_letters, length=15))

        with allure.step("Проверка ошибка авторизации курьера с неправильным паролем"):
            login_response = requests.post(f"{URL_HOME}/api/v1/courier/login", json={
                "login": payload['login'], "password": random_password
            })
            login_response_data = login_response.json()
            expected_response_data = ErrorResponses.NON_EXISTENT_DATA_FOR_LOGIN
            assert login_response.status_code == 404, f'Ожидаем код 404, а получили {login_response.status_code}'
            assert login_response_data == expected_response_data, \
                f'Ожидаем ответ: {expected_response_data}, но получили: {login_response_data}'

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)
