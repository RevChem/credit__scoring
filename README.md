Основная цель построенной системы — оценка кредитоспособности клиентов на основе их анкетных данных с последующим принятием решения о выдаче займа. Вся информация о клиентах хранится в PostgreSQL, что обеспечивает надёжное и масштабируемое управление данными. Через API реализованы операции добавления, редактирования, удаления и получения информации о клиентах, что позволяет легко интегрировать систему в существующие бизнес-процессы или веб-интерфейсы.

В качестве основных моделей используются XGBoost и TabTransformer (в FastApi интегрирован лишь XGBoost). Процесс обучения и дообучения модели организован с использованием MLflow и Optuna. 

В проекте также реализован эндпоинт для анализа дрейфа признаков с использованием библиотеки Evidently. Это дает возможность отслеживать изменения в распределении входных данных с течением времени. 

### Структура проекта

```
credit_scoring/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── main.py                 # Инициализация API
│   │   │   └── routes/
│   │   │       ├── predict.py          # Эндпоинт предсказания
│   │   │       ├── training.py         # Дообучение модели
│   │   │       ├── mlflow_router.py    # Работа с MLflow
│   │   │       ├── dreif.py            # Мониторинг дрейфа (Evidently)
│   │   │       └── interpretation.py   # Интерпретация результатов
│   │   └── logging_config.yaml         # Конфигурация логов
│   │
│   ├── services/
│   │   ├── data_preprocessing.py       # Обработка данных
│   │   ├── drift_detection.py          # Анализ дрейфа признаков
│   │   ├── load_model.py               # Загрузка модели
│   │   └── __init__.py
│   │
│   ├── users/
│   │   ├── models.py                   # ORM-модель пользователя
│   │   ├── schemas.py                  # Pydantic-схемы
│   │   ├── dao.py                      # Доступ к данным
│   │   ├── router.py                   # Роуты пользователей
│   │   ├── rb.py                       # Роли и права
│   │   └── sql_enums.py                # ENUM'ы для БД
│   │
│   ├── database.py                     # Подключение к PostgreSQL
│   ├── config.py                       # Настройки приложения
│   ├── dao/
│   │   └── base.py                     # Базовый DAO
│   └── __init__.py
│
├── data/
│   ├── applications.csv                # Данные о заявках
│   ├── features.csv                    # Описание признаков
│   ├── dataset_columns.json            # Структура данных
│   └── loan_purposes.json              # Цели кредита
│
├── data_modified/                      # Обработанные данные (опционально)
│   ├── original.csv
│   └── modified (2).csv
│
├── models/
│   ├── xgboost/
│   │   └── latest.pkl                  # Обученная модель XGBoost
│   └── tab_transformer/
│       └── latest.pth                  # Модель-заглушка (можно расширить)
│
├── notebooks/
│   └── Кредитный_скоринг.ipynb        # Jupyter-ноутбук с анализом
│
├── migration/                          # Миграции Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── *.py                        # Файлы миграций
│
├── mlruns/                             # Эксперименты MLflow
│   └── [run_id]/...                    # Автогенерируемые данные
│
├── mlartifacts/                        # Артефакты MLflow (модели, графики)
│   └── [model]/artifacts/
│       ├── model/
│       └── shap_summary_plot.png
│
├── drift_report.html                   # Отчёт Evidently (генерируется)
│
├── alembic.ini                         # Конфигурация Alembic
├── .env                                # Переменные окружения
├── .gitignore
├── requirements.txt
└── README.md
```
