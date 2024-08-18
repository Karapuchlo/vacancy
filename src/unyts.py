import requests
import json
from abc import ABC, abstractmethod

class Vacancy:
    def __init__(self, employer_name, name, salary, alternate_url):
        self.employer_name = employer_name
        self.name = name
        self.salary = salary
        self.alternate_url = alternate_url

    def __str__(self):
        return f"Вакансия {self.name} в {self.employer_name} с зарплатой {self.salary}"

    def __repr__(self):
        return f"Vacancy(employer_name='{self.employer_name}', name='{self.name}', salary='{self.salary}', alternate_url='{self.alternate_url}')"

    @property
    def dict(self):
        return {
            'employer_name': self.employer_name,
            'name': self.name,
            'salary': self.salary,
            'alternate_url': self.alternate_url
        }

class VacancyParser(ABC):
    @abstractmethod
    def fetch_vacancies(self):
        """Получить список вакансий"""
        pass

    @abstractmethod
    def export_vacancies(self, vacancies, filename):
        """Экспортировать список вакансий в файл"""
        pass

class HHAPIParser(VacancyParser):
    def fetch_vacancies(self):
        # Задаем параметры запроса
        vacancies = []
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
            for vacancy_data in response.json()['items']:
                if vacancy_data['salary'] is not None:
                    vacancy = Vacancy(
                        vacancy_data["name"],
                        vacancy_data["employer"]["name"],
                        vacancy_data['salary'],
                        vacancy_data["alternate_url"]
                    )
                    vacancies.append(vacancy)

        # Возвращаем список вакансий
        return vacancies

    def export_vacancies(self, vacancies, filename='vacancies.json'):
        # Экспортируем вакансии в json-файл
        with open(filename, 'w', encoding="UTF-8") as jsonfile:
            json.dump([v.dict for v in vacancies], jsonfile, indent=4, ensure_ascii=False)


def run_parser_hh():
    parser_hh = HHAPIParser()
    vacancies = parser_hh.fetch_vacancies()
    parser_hh.export_vacancies(vacancies)
    return vacancies


def run_parser_Superjob():
    parser_Superjob = SuperjobAPIParser()
    vacancies = parser_Superjob.fetch_vacancies()
    parser_Superjob.export_vacancies(vacancies)
    return vacancies


class SuperjobAPIParser(VacancyParser):
    def __init__(self):
        self.token = self.get_authorization_token()

    def get_authorization_token(self):
        # Задаем параметры запроса
        params = {
            'login': 'mc_gra_dy@mail.ru',
            'password': '240615Nastya',
            'client_id': '2270',
            'client_secret': 'v3.r.137463232.a085bb1aaa3c51a9b7b88481b7075aa785b24619.5bc49efdee8512297bdf804e2d7b7cc7f3736ec3',
            'scope': 'api'
        }

        # Отправляем POST-запрос на получение токена авторизации
        auth_url = 'https://api.superjob.ru/2.0/oauth2/password/'
        response = requests.post(auth_url, params=params)

        # Возвращаем токен авторизации
        return response.json()['access_token']

    def fetch_vacancies(self, salary_from=None):

        # Задаем параметры запроса
        headers = {
            'X-Api-App-Id': 'v3.r.137463232.a085bb1aaa3c51a9b7b88481b7075aa785b24619.5bc49efdee8512297bdf804e2d7b7cc7f3736ec3'}
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
                vacancy = Vacancy(
                    employer_name=vacancy_data['profession'],
                    name=vacancy_data['firm_name'],
                    salary=vacancy_data['payment_from'],
                    alternate_url=vacancy_data['link']
                )
                vacancies.append(vacancy)
        # Возвращаем список вакансий
        return vacancies

    def export_vacancies(self, vacancies, filename='vacancies_superjob.json'):
        # Экспортируем вакансии в json-файл
        with open(filename, 'w', encoding="UTF-8") as jsonfile:
            json.dump([v.dict for v in vacancies], jsonfile, indent=4, ensure_ascii=False)
