
from dataclasses import dataclass

@dataclass
class Vacancy:
    employer_name: str
    name: str
    salary: str
    alternate_url: str

class Vacancy:
    def __init__(self, employer_name, name, salary, alternate_url):
        self.employer_name = employer_name
        self.name = name
        self.salary = salary
        self.alternate_url = alternate_url

    def __repr__(self):
        return f"Вакансия {self.employer_name} с зарплатой {self.salary}\n"

    def to_dict(self):
        return {
            'employer_name': self.employer_name,
            'name': self.name,
            'salary': self.salary,
            'alternate_url': self.alternate_url
        }
