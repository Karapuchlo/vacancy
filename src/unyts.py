# parser
import requests
import csv
import json
from src.vacancy import Vacancy

class HHAPIParser:
    def fetch_vacancies_hh(self):
    # Задаем параметры запроса
        for i in range(10):
            params = {
                'text': 'Python разработчик',
                'area': 113,  # 113 - Россия
                'page': i,
                'per_page': 100  # количество возвращаемых вакансий на странице
            }

            # Отправляем GET-запрос на получение списка вакансий
            vacancies_url = 'https://api.hh.ru/vacancies'
            headers = {
                'User-Agent': 'HH-User-Agent',
                'accept': 'application/json, text/plain, */*',
            }
            response = requests.get(vacancies_url, headers=headers, params=params)
            data = response.content.decode()
            response.close()
            js_hh = json.loads(data)

            # Обрабатываем полученные данные
            vacancies = []
            for vacancy_data in response.json()['items']:
                if vacancy_data['salary'] is not None:
                    vacancy = Vacancy(vacancy_data["name"], vacancy_data["employer"]["name"], vacancy_data['salary'], vacancy_data["alternate_url"])
                    vacancies.append(vacancy)

            # Возвращаем список вакансий
            return vacancies


# exporter
    def export_vacancies_hh(self, vacancies):
        # Экспортируем вакансии в json-файл
        with open('vacancies.json', 'w', encoding="UTF-8") as jsonfile:
            json.dump([v.__dict__ for v in vacancies], jsonfile, indent=4, ensure_ascii=False)


class HHAPIExporter:
    pass



# superjob_api_parser.py
class SuperjobAPIParser:
    def __init__(self):
        # Получаем токен авторизации приложения
        self.token = self.get_authorization_token()

    def get_authorization_token(self):
        # Задаем параметры запроса
        params = {'login': 'mc_gra_dy@mail.ru', 'password': '240615Nastya', 'client_id': '2270', 'client_secret': 'v3.r.137463232.a085bb1aaa3c51a9b7b88481b7075aa785b24619.5bc49efdee8512297bdf804e2d7b7cc7f3736ec3', 'scope': 'api'}

        # Отправляем POST-запрос на получение токена авторизации
        auth_url = 'https://api.superjob.ru/2.0/oauth2/password/'
        response = requests.post(auth_url, params=params)

        # Возвращаем токен авторизации
        return response.json()['access_token']

    def fetch_vacancies_Superjob(self, salary_from = '60000'):
        # Задаем параметры запроса
        headers = {'X-Api-App-Id': 'v3.r.137463232.a085bb1aaa3c51a9b7b88481b7075aa785b24619.5bc49efdee8512297bdf804e2d7b7cc7f3736ec3'}
        params = {'keywords': 'Python разработчик', 'count': '100'}

        # Отправляем GET-запрос на получение списка вакансий
        if salary_from:
            # Если указана только зарплата "от"
            params['payment_from'] = salary_from
            vacancies_url = 'https://api.superjob.ru/2.0/vacancies/?payment_from=%s' % salary_from
        else:
            # Если зарплата не указана
            vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'

        # Отправляем запрос
        response = requests.get(vacancies_url, headers=headers, params=params)

        # Обрабатываем полученные данные
        vacancies = []
        for vacancy_data in response.json()['objects']:
            if vacancy_data['payment_from'] is not None:
                vacancy = Vacancy(employer_name=vacancy_data['profession'], name=vacancy_data['firm_name'], salary=vacancy_data['payment_from'], alternate_url=vacancy_data['link'])
                vacancies.append(vacancy)
        # Возвращаем список вакансий
        return vacancies


class SuperjobAPIExporter:
    pass

def run_parser_hh():
    # Создаем экземпляр парсера
    parser_hh = HHAPIParser()

    # Получаем вакансии через API
    vacancies_hh = parser_hh.fetch_vacancies_hh()
    print(vacancies_hh)

    # Создаем экземпляр экспортера
    exporter_hh = HHAPIExporter()
    print(exporter_hh)
    # Экспортируем данные в нужном формате
    parser_hh.export_vacancies_hh(vacancies_hh)

def run_parser_Superjob():
    # Создаем экземпляр парсера
    parser_Superjob = SuperjobAPIParser()
    parser_hh = HHAPIParser()

    # Получаем вакансии через API
    vacancies_Superjob = parser_Superjob.fetch_vacancies_Superjob()
    print(vacancies_Superjob)

    # Создаем экземпляр экспортера
    exporter_Superjob = HHAPIExporter()
    print(exporter_Superjob)
    # Экспортируем данные в нужном формате
    parser_hh.export_vacancies_hh(vacancies_Superjob)