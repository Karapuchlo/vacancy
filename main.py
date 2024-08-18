import json
from src.unyts import run_parser_hh, run_parser_Superjob
from src.vacancy import Vacancy
def main():
    while True:
        # Выводим список доступных действий
        print('1. Парсить вакансии')
        print('2. Выход')

        # Запрашиваем у пользователя номер действия
        action = input('Введите номер действия: ')

        # Выполняем соответствующее действие
        if action == '1':
            # Парсим вакансии
            print('С какого сайта парсим?')
            print("1. HH")
            print("2. Superjob")
            viborparsera = input('Введите номер сайта: ')
            if viborparsera == '1':
                vacancies = run_parser_hh()
            elif viborparsera == '2':
                vacancies = run_parser_Superjob()

                # Сериализуем список вакансий в JSON
                with open('vacancies.json', 'w', encoding='utf-8') as f:
                    json.dump([v.__dict__ for v in vacancies], f, ensure_ascii=False, indent=4)

            # Экспортируем вакансии
            print('Данные успешно экспортированы в файл vacancies.json')
            break
        elif action == '2':
            # Выйти из программы
            break
        else:
            print('Неправильный выбор.')

if __name__ == '__main__':
    main()
