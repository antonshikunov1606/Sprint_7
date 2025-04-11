import allure
import pytest
import requests
from test_data import URLS, credentials
from response_definitions import SuccessResponses, ErrorResponses


class TestCreateCourier:
    @allure.title("Проверка создания нового курьера с правильными данными")
    def test_create_new_courier_with_all_valid_data(self, get_id_courier, delete_courier):
        payload = credentials

        with allure.step("Регистрация нового курьера"):
            reg_response = requests.post(URLS['courier'], json=payload)
            reg_response_data = reg_response.json()
            expected_response_data = SuccessResponses.SUCCESSFUL_REGISTRATION
            assert reg_response.status_code == 201, f'Ожидаем код 201, но получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}, но получили: {reg_response_data}."

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности создания уже существующего курьера")
    def test_create_courier_with_existing_credentials_not_allowed(self, get_id_courier, delete_courier):
        payload = credentials

        with allure.step("Регистрация нового курьера"):
            reg_response = requests.post(URLS['courier'], json=payload)

        #  повторно пробуем зарегистрировать этого курьера
        with allure.step("Проверка ошибки повторной регистрации курьера с одинаковыми данными"):
            reg_response = requests.post(URLS['courier'], json=payload)
            reg_response_data = reg_response.json()
            expected_response_data = ErrorResponses.LOGIN_IS_ALREADY_USING
            assert reg_response.status_code == 409, f'Ожидаем код 409, но получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}', но получили: {reg_response_data}."

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности создания курьера с недостаточными данными")
    @pytest.mark.parametrize("partial_payload", [
        {"password": credentials["password"]},
        {"login": credentials["login"]}
    ])
    def test_create_courier_without_login_or_password_not_allowed(self, partial_payload):
        with allure.step("Проверка ошибка регистрации курьера с недостаточными данными"):
            reg_response = requests.post(URLS['courier'], json=partial_payload)
            reg_response_data = reg_response.json()
            expected_response_data = ErrorResponses.INSUFFICIENT_DATA_FOR_REGISTRATION
            assert reg_response.status_code == 400, f'Ожидаем код 400, а получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f'Ожидаем ответ: {expected_response_data}, но получили: {reg_response_data}'

    @allure.title("Проверка невозможности создания курьера с зарегистрированными логином")
    def test_create_courier_with_the_same_login_not_allowed(self, get_id_courier, delete_courier):
        payload = credentials

        with allure.step("Регистрация нового курьера"):
            reg_response = requests.post(URLS['courier'], json=payload)

        #  пробуем создать нового курьера с тем же логином
        with allure.step("Проверка ошибки регистрации курьера с тем же логином"):
            reg_response = requests.post(URLS['courier'], json={
                "login": payload['login'], "password": "qwe161616", "firstName": "Alexey"})
            reg_response_data = reg_response.json()
            expected_response_data = ErrorResponses.LOGIN_IS_ALREADY_USING
            assert reg_response.status_code == 409, f'Ожидаем код 409, но получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}', но получили: {reg_response_data}."

        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        with allure.step("Удаление курьера"):
            delete_courier(id_courier)
