import os
import openai
import streamlit as st
from parse_hh import get_candidate_info, get_job_description

# Установка API ключа
openai.api_key = os.getenv("OPENAI_API_KEY")  # Или используйте st.secrets["api_keys"]["OPENAI_API_KEY"]

# Системный промпт
SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
""".strip()


# Функция для отправки запроса в OpenAI API
def request_gpt(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Убедитесь, что модель доступна
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            temperature=0,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Ошибка при обращении к OpenAI API: {str(e)}"


# Интерфейс Streamlit
st.title("CV Scoring App")

# Ввод данных
job_description_url = st.text_area("Введите ссылку на описание вакансии")
cv_url = st.text_area("Введите ссылку на резюме")

# Кнопка для анализа
if st.button("Оценить резюме"):
    with st.spinner("Производится анализ..."):
        try:
            # Получение данных о вакансии и резюме
            job_description = get_job_description(job_description_url)
            cv = get_candidate_info(cv_url)

            # Отображение данных
            st.subheader("Описание вакансии:")
            st.write(job_description)
            st.subheader("Резюме:")
            st.write(cv)

            # Подготовка запроса
            user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
            response = request_gpt(SYSTEM_PROMPT, user_prompt)

            # Отображение результата
            st.subheader("Результат анализа:")
            st.write(response)

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")