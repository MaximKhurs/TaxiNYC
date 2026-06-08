FROM apache/airflow:2.10.5

# Переключаемся на пользователя root для установки пакетов
USER root

# Устанавливаем системные зависимости (для psycopg2 и pyarrow)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Возвращаемся на пользователя airflow
USER airflow

# Устанавливаем Python-библиотеки
RUN pip install --no-cache-dir \
    pandas \
    pyarrow \
    requests