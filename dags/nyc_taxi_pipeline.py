# Даг для проверки и загрузки новых данных 


from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


import sys
sys.path.append('/opt/airflow/scripts')
from download_taxi_data import check_and_download


default_args = {
    'owner': 'data_engineer',          # Владелец (ты)
    'depends_on_past': False,          # Не ждать предыдущий запуск
    'retries': 2,                      # Сколько раз повторять при ошибке
    'retry_delay': timedelta(minutes=5),  # Пауза между повторами
}

# Создаём DAG
with DAG(
    'nyc_taxi_daily_load',             # Уникальное имя DAG'а
    default_args=default_args,
    description='Ежедневная загрузка данных NYC Taxi',
    schedule_interval='@daily',         # Запуск каждый день в полночь
    start_date=datetime(2026, 6, 1),   # С какой даты начинать
    catchup=False,                      # Не запускать пропущенные дни
    tags=['nyc_taxi', 'learning'],     # Теги для удобства в интерфейсе
) as dag:

    # Таск "начало" — просто для красоты
    start = EmptyOperator(
        task_id='start'
    )

    # Таск "скачать данные" — вызывает нашу Python-функцию
    download_data = PythonOperator(
        task_id='download_taxi_data',
        python_callable=check_and_download,
    )

    # Таск "конец"
    end = EmptyOperator(
        task_id='end'
    )

    # Порядок выполнения: start → download → end
    start >> download_data >> end
