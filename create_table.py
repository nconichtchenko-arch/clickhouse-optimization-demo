import clickhouse_connect
import random
from datetime import datetime, timedelta

# Подключаемся к ClickHouse (через проброс портов VirtualBox)
client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='dwh_user',
    password='dwh_password'
)

# Создаем таблицу (пока без оптимизации)
client.command("""
    CREATE TABLE IF NOT EXISTS sales_raw (
        id UInt64,
        order_date Date,
        customer_id UInt32,
        product_id UInt32,
        quantity UInt32,
        price Float64,
        total_amount Float64,
        region String
    ) ENGINE = MergeTree()
    ORDER BY id
""")

print("✅ Таблица sales_raw создана (без оптимизации).")

# Генерируем 1 млн строк
print("⏳ Генерация 1 млн строк...")
rows = []
start_date = datetime(2026, 1, 1)
regions = ["Москва", "СПб", "Воронеж", "Казань", "Новосибирск"]

for i in range(1_000_000):
    order_date = start_date + timedelta(days=random.randint(0, 300))
    customer_id = random.randint(1, 10000)
    product_id = random.randint(1, 1000)
    quantity = random.randint(1, 10)
    price = round(random.uniform(10.0, 1000.0), 2)
    total_amount = quantity * price
    region = random.choice(regions)
    rows.append((i, order_date.date(), customer_id, product_id, quantity, price, total_amount, region))

print("⏳ Вставка данных...")
client.insert('sales_raw', rows, column_names=[
    'id', 'order_date', 'customer_id', 'product_id', 'quantity', 'price', 'total_amount', 'region'
])
print("✅ Данные загружены в sales_raw.")