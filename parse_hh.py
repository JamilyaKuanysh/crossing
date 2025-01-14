import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    """Отправляет запрос и возвращает HTML страницы."""
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    ).text

def extract_vacancy_data(html: str) -> str:
    """Извлекает данные о вакансии и возвращает их в формате Markdown."""
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Заголовок вакансии не найден"

    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Компания не указана"

    salary = soup.find("span", {"data-qa": "vacancy-salary"})
    salary = salary.text.strip() if salary else "Зарплата не указана"

    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Требуемый опыт не указан"

    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Тип занятости не указан"

    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location.text.strip() if location else "Местоположение не указано"

    description = soup.find("div", {"data-qa": "vacancy-description"})
    description = description.text.strip() if description else "Описание вакансии отсутствует"

    skills_section = soup.find("div", {"data-qa": "bloko-tag-list"})
    skills = [skill.text.strip() for skill in skills_section.find_all("span", {"data-qa": "bloko-tag__text"})] if skills_section else []

    return f"""
# {title}

**Компания:** {company}  
**Зарплата:** {salary}  
**Опыт работы:** {experience}  
**Тип занятости:** {employment_mode}  
**Местоположение:** {location}  

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills) if skills else 'Навыки не указаны'}
""".strip()

def extract_candidate_data(html: str) -> str:
    """Извлекает данные о кандидате и возвращает их в формате Markdown."""
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find("h1", {"data-qa": "resume-header-title"})
    name = name.text.strip() if name else "Имя не найдено"

    gender_age = soup.find("div", {"data-qa": "resume-personal-gender-age"})
    gender_age = gender_age.text.strip() if gender_age else "Пол и возраст не найдены"

    location = soup.find("span", {"data-qa": "resume-personal-address"})
    location = location.text.strip() if location else "Местоположение не найдено"

    job_title = soup.find("span", {"data-qa": "resume-block-title-position"})
    job_title = job_title.text.strip() if job_title else "Должность не найдена"

    job_status = soup.find("span", {"data-qa": "resume-block-status"})
    job_status = job_status.text.strip() if job_status else "Статус не найден"

    experience_section = soup.find("div", {"data-qa": "resume-block-experience"})
    experiences = []
    if experience_section:
        for item in experience_section.find_all("div", {"class": "resume-block-item-gap"}):
            company = item.find("div", {"class": "bloko-text_strong"})
            company = company.text.strip() if company else "Компания не указана"

            position = item.find("div", {"data-qa": "resume-block-experience-position"})
            position = position.text.strip() if position else "Должность не указана"

            description = item.find("div", {"data-qa": "resume-block-experience-description"})
            description = description.text.strip() if description else "Описание не указано"

            experiences.append(f"**Компания:** {company}\n**Должность:** {position}\n{description}")

    skills_section = soup.find("div", {"data-qa": "skills-table"})
    skills = [skill.text.strip() for skill in skills_section.find_all("span", {"data-qa": "bloko-tag__text"})] if skills_section else []

    return f"""
# {name}

**Пол и возраст:** {gender_age}  
**Местоположение:** {location}  
**Должность:** {job_title}  
**Статус:** {job_status}  

## Опыт работы
{'\n\n'.join(experiences) if experiences else 'Опыт работы отсутствует'}

## Ключевые навыки
- {'\n- '.join(skills) if skills else 'Навыки отсутствуют'}
""".strip()

def get_candidate_info(url: str) -> str:
    """Получает данные о кандидате с указанного URL."""
    html = get_html(url)
    return extract_candidate_data(html)

def get_job_description(url: str) -> str:
    """Получает данные о вакансии с указанного URL."""
    html = get_html(url)
    return extract_vacancy_data(html)