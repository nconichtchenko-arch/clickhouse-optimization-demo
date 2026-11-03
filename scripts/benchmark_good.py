import clickhouse_connect
import time

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='dwh_user',
    password='dwh_password'
)

print("🔍 Замер «хорошего» запроса (оптимизированная таблица sales_optimized)...")

# Тот же запрос, но на оптимизированной таблице
start = time.time()
result = client.query("""
    SELECT region, count(*), sum(total_amount)
    FROM sales_optimized
    WHERE region = 'Москва'
    GROUP BY region
""")
end = time.time()

print(f"⏱ Время выполнения: {end - start:.2f} сек")
for row in result.result_rows:
    print(f"   Region: {row[0]}, Count: {row[1]}, Sum: {row[2]:.2f}")
