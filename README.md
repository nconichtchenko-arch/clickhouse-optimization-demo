# ClickHouse Optimization Demo

Демонстрация оптимизации запросов в ClickHouse: партиционирование, сортировка и сравнение производительности.

## Что это такое?

ClickHouse — колоночная СУБД для аналитики. Но даже она может работать медленно, если таблица создана неправильно. В этом проекте показано, как **партиционирование** и **правильный `ORDER BY`** ускоряют запросы.

## Что реализовано

- **Таблица `sales_raw`** (без оптимизации): `ORDER BY id`, без партиционирования.
- **Таблица `sales_optimized`** (с оптимизацией): `PARTITION BY toYYYYMM(order_date)`, `ORDER BY (region, order_date, id)`.
- **Скрипт `create_table.py`**: создает `sales_raw` и загружает 1 млн строк.
- **Скрипт `optimize_table.py`**: создает `sales_optimized` и переносит данные.
- **Скрипт `benchmark_bad.py`**: замеряет «плохой» запрос (фильтр по `region`, который не в `ORDER BY`).
- **Скрипт `benchmark_good.py`**: замеряет тот же запрос на оптимизированной таблице.

## Стек

- ClickHouse (Docker)
- Python (clickhouse-connect)
- Docker

## Результаты

| Запрос | Таблица | Время |
|---|---|---|
| Фильтр по `region = 'Москва'` | `sales_raw` (без оптимизации) | **0.21 сек** |
| Фильтр по `region = 'Москва'` | `sales_optimized` (с оптимизацией) | **0.15 сек** |

**Ускорение:** ~1.4x (на 1 млн строк). В реальных проектах с 100+ млн строк ускорение может быть в разы больше.

## Как запустить

**1. Поднимите ClickHouse в Docker (внутри VM):**

    cd ~/clickhouse-demo
    sudo docker compose up -d

**2. Установите зависимости:**

    pip install clickhouse-connect

**3. Создайте таблицу и загрузите данные:**

    cd scripts
    python create_table.py

**4. Оптимизируйте таблицу:**

    python optimize_table.py

**5. Замерьте «плохой» и «хороший» запросы:**

    python benchmark_bad.py
    python benchmark_good.py

## 🔬 Сравнение с Greenplum (MPP Benchmark)

В рамках изучения MPP-СУБД был проведен бенчмарк: загрузка 397 924 строк (e-commerce) и аналитический запрос (`GROUP BY` + `SUM`).

| Этап | ClickHouse | Greenplum |
| :--- | :--- | :--- |
| **Загрузка** | 18.63 сек. | 206.99 сек. |
| **Аналитический запрос** | 0.1207 сек. | 0.7711 сек. |

**Результат:** ClickHouse загрузил данные в **11 раз** быстрее и выполнил запрос в **6.39 раз** быстрее. Это подтверждает преимущество колоночной архитектуры для OLAP-задач.

*Код бенчмарка (`benchmark.py`) находится в корне этого репозитория. Аналогичный код и результаты доступны в [greenplum-dwh-demo](https://github.com/nconichtchenko-arch/greenplum-dwh-demo).*

## Ссылки

- [Основной проект DWH Marketplace Analytics](https://github.com/nconichtchenko-arch/marketplace-dwh-analytics)
- [Data Contracts Demo](https://github.com/nconichtchenko-arch/data-contracts-demo)
- [dbt CI/CD Demo](https://github.com/nconichtchenko-arch/dbt-ci-cd-demo)
- [dbt + Great Expectations Demo](https://github.com/nconichtchenko-arch/dbt-great-expectations-demo)
