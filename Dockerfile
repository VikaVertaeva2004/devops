# В качестве основы используется Ubuntu OS (version 20.04)
FROM ubuntu:20.04
# Указываем авторов проекта
LABEL authors="Vertaeva Viktoriya 221-351"
# Устанавливаем временную зону
ENV TZ=Europe/Moscow 
# Создаем дикректорию для проекта
WORKDIR /app
# Копируем все файлы из текущей директории в папку с проектом
COPY . .
# Синхронизируем данные и устанавливаем необходимые пакеты, а также зависимости
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update -y && apt-get install -y --no-install-recommends \
    python3-pip build-essential \
    python3-dev default-libmysqlclient-dev \
    pkg-config \
    gunicorn && \
    # Удаляем ненужные установочные файлы
    apt-get clean && \
    # Очищаем кэш apt list
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir -r requirements.txt
WORKDIR /app/ppp
# Задаем команду для запуска
CMD /usr/bin/gunicorn -b 0.0.0.0:80 -w 4 app:app
