import clickhouse_connect

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='dwh_user',
    password='dwh_password'
)

print("🔧 Создаем оптимизированную таблицу sales_optimized...")

# Создаем таблицу с партиционированием по месяцу и ORDER BY (region, order_date)
client.command("""
    CREATE TABLE IF NOT EXISTS sales_optimized (
        id UInt64,
        order_date Date,
        customer_id UInt32,
        product_id UInt32,
        quantity UInt32,
        price Float64,
        total_amount Float64,
        region String
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(order_date)
    ORDER BY (region, order_date, id)
""")

print("✅ Таблица sales_optimized создана.")

# Переносим данные из sales_raw в sales_optimized
print("⏳ Перенос данных из sales_raw в sales_optimized...")
client.command("""
    INSERT INTO sales_optimized
    SELECT * FROM sales_raw
""")
print("✅ Данные перенесены.")