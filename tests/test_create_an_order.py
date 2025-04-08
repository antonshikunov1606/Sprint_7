import allure
import pytest
import requests
import test_data
from response_definitions import SuccessResponses, ErrorResponses

URL_HOME = 'https://qa-scooter.praktikum-services.ru/'


class TestCreateAnOrder:
    @allure.title("Проверка создания заказа")
    @pytest.mark.parametrize("test_data_for_order", test_data.data_for_order)
    def test_create_an_order_success(self, test_data_for_order):
        with allure.step("Проверка создания заказа"):
            order_response = requests.post(f'{URL_HOME}/api/v1/orders', json=test_data_for_order)
            response_data = order_response.json()
            track = response_data["track"]
            expected_response_data = SuccessResponses.success_ordered(track)
            assert order_response.status_code == 201, f'Ожидаем код 201, но получили {order_response.status_code}'
            assert response_data == expected_response_data, \
                f"Ожидаем ответ: {expected_response_data}, но получили: {response_data}"
