
import os
import requests
from datetime import datetime, timedelta


def check_and_download():
    """
    Проверяет наличие данных за последний доступный месяц
    и скачивает, если их ещё нет локально.

    """
    # Берём дату с отступом в 2 месяца назад
    target_date = datetime.now() - timedelta(days=60)
    year = 2025
    month = 1

    file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
    raw_path = f"/opt/airflow/data/raw/{file_name}"

    # Создаём папку, если её нет
    os.makedirs("/opt/airflow/data/raw", exist_ok=True)

    # Проверяем, не скачан ли уже файл
    if os.path.exists(raw_path):
        print(f"Файл {file_name} уже скачан. Пропускаем.")
        return file_name

    # Скачиваем
    print(f"Скачиваю {file_name}...")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(raw_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Скачан {file_name}")
        return file_name
    else:
        print(f"Файл {file_name} пока недоступен (код {response.status_code})")
        return None


if __name__ == "__main__":
    result = check_and_download()
    if result:
        print(f"Готово: {result}")
    else:
        print("Новых данных нет.")