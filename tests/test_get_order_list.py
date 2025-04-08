import json
import allure
import pytest
import requests
from response_definitions import SuccessResponses, ErrorResponses

URL_HOME = 'https://qa-scooter.praktikum-services.ru/'


class TestGetOrderList:
    @allure.title("Проверка получения списка заказов по фильтру станций метро")
    def test_get_order_list_with_param_nearest_station_show_with_certain_station(self):
        params = {
            'nearestStation': json.dumps(["6"])
        }
        list_response = requests.get(f'{URL_HOME}/api/v1/orders', params=params)
        response_data = list_response.json()
        metro_station = response_data['availableStations'][0]['name']
        expected_result = 'Комсомольская'
        assert list_response.status_code == 200, f'Ожидаем код 200, но получили {list_response.status_code}'
        assert 'orders' in response_data
        assert type(response_data['orders']) is list
        assert metro_station == expected_result, f'Ожидаем станцию {expected_result}, но получили {metro_station}'

    @allure.title("Проверка получения списка заказов с указанием лимита")
    def test_get_order_list_with_param_limit_show_orders_with_limit(self):
        params = {
            'limit': 5
        }
        list_response = requests.get(f'{URL_HOME}/api/v1/orders', params=params)
        response_data = list_response.json()
        limit = response_data['pageInfo']['limit']
        expected_result = params['limit']
        assert list_response.status_code == 200, f'Ожидаем код 200, но получили {list_response.status_code}'
        assert 'orders' in response_data
        assert type(response_data['orders']) is list
        assert limit == expected_result, f'Ожидаем лимит {expected_result}, но получили {limit}'

    @allure.title("Проверка получения списка заказов с указанием текущей страницы")
    def test_get_order_list_with_param_page_show_current_page(self):
        params = {
            'page': 2
        }
        list_response = requests.get(f'{URL_HOME}/api/v1/orders', params=params)
        response_data = list_response.json()
        current_page = response_data['pageInfo']['page']
        expected_result = params['page']
        assert list_response.status_code == 200, f'Ожидаем код 200, но получили {list_response.status_code}'
        assert 'orders' in response_data
        assert type(response_data['orders']) is list
        assert current_page == expected_result, f'Ожидаем лимит {expected_result}, но получили {current_page}'
