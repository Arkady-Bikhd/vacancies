import requests
from itertools import count
from time import sleep
from dotenv import load_dotenv
from os import environ
from terminaltables import AsciiTable


def main():
    load_dotenv()
    superjob_api_key = environ['SUPERJOB_API_KEY']
    languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++',
        'Go', 'Shell', 'Scala', 'Swift']
    try:
       print_salary_statistic(get_avg_salary_hh(languages), 'HeadHunter Moscow')       
    except requests.HTTPError:
        print('Ошибка обращения к сайту hh.ru')
    try:
        print_salary_statistic(get_avg_salary_superjob(languages, superjob_api_key), 'SuperJob Moscow')
    except requests.HTTPError:
        print('Ошибка обращения к сайту SuperJob.ru или неверный api_key')


def get_vacancies_hh(language, page):

    area = 4
    period = 30
    payload = {
        'text': f'Программист {language}',
        'area': area,
        'period': period,
        'page': page,
        'per_page': 100
        }
    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_avg_salary_hh(languages):
    
    avg_salary_by_language = dict()
    found = 0
    for language in languages:        
        salary_by_language = list()        
        for page in count(0):            
            vacancy = get_vacancies_hh(language, page) 
            for salary in vacancy['items']:
                salary = salary['salary']
                if salary:            
                    salary_by_language.append(salary)
            sleep(0.25)
            if page >= vacancy['pages'] - 1:
                found = vacancy['found']
                break                           
        vacancy_proceed, avg_salary = count_salary(salary_by_language, predict_rub_salary_for_hh)               
        avg_salary_by_language[language] = create_salary_data_by_language(found, vacancy_proceed, avg_salary)
    return avg_salary_by_language


def predict_rub_salary_for_hh(vacancy):
        
    avr_salary = None
    from_salary = vacancy['from']
    to_salary = vacancy['to']
    if vacancy['currency']  != 'RUR':
        return 
    if vacancy['currency']:
        if from_salary and to_salary:
            avr_salary = (from_salary + to_salary) / 2
        elif from_salary:
            avr_salary = 1.2 * from_salary
        elif to_salary:
            avr_salary = 0.8 * to_salary
    
    return avr_salary     


def get_vacancies_superjob(api_key, language, page):
    
    headers = {
        'X-Api-App-Id': api_key
    }
    town = 4
    catalogue = 48
    params = {
        't': town,
        'catalogues': catalogue,
        'keyword': f'Программист {language}',
        'page' : page,
        'count' : 100,    
    }
    response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)    
    response.raise_for_status()
      
    return response.json() 

def get_avg_salary_superjob(languages, api_key):
    
    avg_salary_by_language = dict()        
    for language in languages:        
        salary_by_language = list()
        for page in count(0):
            vacancy = get_vacancies_superjob(api_key, language, page)
            more = vacancy['more']
            found = vacancy['total']
            vacancy = vacancy['objects']            
            for salary in vacancy:
                short_salary_data = dict()                
                short_salary_data['payment_from'] = salary['payment_from']
                short_salary_data['payment_to'] = salary['payment_to']
                short_salary_data['currency'] = salary['currency']
                salary_by_language.append(short_salary_data)
            sleep(0.25)
            if not more:
               break
        vacancy_proceed, avg_salary = count_salary(salary_by_language, predict_rub_salary_for_superJob)               
        avg_salary_by_language[language] = create_salary_data_by_language(found, vacancy_proceed, avg_salary)
    return avg_salary_by_language


def count_salary(salary_by_language, get_predict_salary):

    vacancy_proceed = 0
    sum_salary = 0        
    for salary in salary_by_language:
        predict_salary = get_predict_salary(salary)               
        if  predict_salary:
            sum_salary +=  predict_salary
            vacancy_proceed += 1    
    return vacancy_proceed, sum_salary


def create_salary_data_by_language(found, vacancy_proceed, avg_salary):
    
    if vacancy_proceed:
        avg_salary = int(avg_salary / vacancy_proceed) 
    salary_data_by_language = dict()
    salary_data_by_language['vacancies_found'] = found
    salary_data_by_language['vacancies_processed'] = vacancy_proceed
    salary_data_by_language['average_salary'] = avg_salary
    return salary_data_by_language


def predict_rub_salary_for_superJob(vacancy):

    avr_salary = None
    from_salary = vacancy['payment_from']
    to_salary = vacancy['payment_to']    
    if vacancy['currency'] == 'rub':
        if from_salary and to_salary:
            avr_salary = (from_salary + to_salary) / 2
        elif from_salary:
            avr_salary = 1.2 * from_salary
        elif to_salary:
            avr_salary = 0.8 * to_salary
    return avr_salary  


def print_salary_statistic(salary, title):
    
    table_statistic = [
            ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language, language_data in salary.items():
        table_statistic.append(list([language, language_data['vacancies_found'], 
        language_data['vacancies_processed'], language_data['average_salary']]))
    table_instance = AsciiTable(table_statistic, title)    
    print(table_instance.table)
    print()

if __name__ == '__main__':
    main()