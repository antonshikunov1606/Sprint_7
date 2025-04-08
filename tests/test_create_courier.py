import allure
import pytest
import requests
from response_definitions import SuccessResponses, ErrorResponses

URL_HOME = 'https://qa-scooter.praktikum-services.ru/'


class TestCreateCourier:
    @allure.title("Проверка создания нового курьера с правильными данными")
    def test_create_new_courier_with_all_valid_data(self, get_id_courier, delete_courier):
        payload = {
            "login": "anton_shik",
            "password": "qwerty000",
            "firstName": "Anton"
        }

        #  регистрируем нового юзера с тестовыми данными
        with allure.step("Регистрация нового курьера"):
            reg_response = requests.post(f"{URL_HOME}/api/v1/courier", json=payload)
            reg_response_data = reg_response.json()
            expected_response_data = SuccessResponses.SUCCESSFUL_REGISTRATION
            assert reg_response.status_code == 201, f'Ожидаем код 201, но получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}, но получили: {reg_response_data}."

        #  используем фикстуру login_courier и логинимся под созданным юзером чтобы достать его id
        with allure.step("Получение id курьера через авторизацию"):
            id_courier = get_id_courier(payload)

        # используем фикстуру delete_courier чтобы удалить созданного юзера чтобы почистить данные после теста
        with allure.step("Удаление курьера"):
            delete_courier(id_courier)

    @allure.title("Проверка невозможности создания уже существующего курьера")
    def test_create_courier_with_existing_credentials_not_allowed(self, get_id_courier, delete_courier):
        payload = {
            "login": "anton_shik",
            "password": "qwerty000",
            "firstName": "Anton"
        }

        with allure.step("Регистрация нового курьера"):
            reg_response = requests.post(f"{URL_HOME}/api/v1/courier", json=payload)
            reg_response_data = reg_response.json()
            expected_response_data = SuccessResponses.SUCCESSFUL_REGISTRATION
            assert reg_response.status_code == 201, f'Ожидаем код 201, но получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}', но получили: {reg_response_data}."

        #  повторно пробуем зарегистрировать этого курьера
        with allure.step("Проверка ошибки повторной регистрации курьера с одинаковыми данными"):
            reg_response = requests.post(f"{URL_HOME}/api/v1/courier", json=payload)
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
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_login_or_password_not_allowed(self, missing_field):
        payload = {
            "login": "anton_shik",
            "password": "qwerty000",
            "firstName": "Anton"
        }
        payload.pop(missing_field)
        with allure.step("Проверка ошибка регистрации курьера с недостаточными данными"):
            reg_response = requests.post(f"{URL_HOME}/api/v1/courier", json=payload)
            reg_response_data = reg_response.json()
            expected_response_data = ErrorResponses.INSUFFICIENT_DATA_FOR_REGISTRATION
            assert reg_response.status_code == 400, f'Ожидаем код 400, а получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f'Ожидаем ответ: {expected_response_data}, но получили: {reg_response_data}'

    @allure.title("Проверка невозможности создания курьера с зарегистрированными логином")
    def test_create_courier_with_the_same_login_not_allowed(self, get_id_courier, delete_courier):
        payload = {
            "login": "anton_shik",
            "password": "qwerty000",
            "firstName": "Anton"
        }

        with allure.step("Регистрация нового курьера"):
            reg_response = requests.post(f"{URL_HOME}/api/v1/courier", json=payload)
            reg_response_data = reg_response.json()
            expected_response_data = SuccessResponses.SUCCESSFUL_REGISTRATION
            assert reg_response.status_code == 201, f'Ожидаем код 201, но получили {reg_response.status_code}'
            assert reg_response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}', но получили: {reg_response_data}."

        #  пробуем создать нового курьера с тем же логином
        with allure.step("Проверка ошибки регистрации курьера с тем же логином"):
            reg_response = requests.post(f"{URL_HOME}/api/v1/courier", json={
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
