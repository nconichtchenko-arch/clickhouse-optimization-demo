import clickhouse_connect
import time

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='dwh_user',
    password='dwh_password'
)

print("🔍 Замер «плохого» запроса (фильтр по region, который не в ORDER BY)...")

# «Плохой» запрос: фильтруем по region, но в таблице ORDER BY id, 
# поэтому ClickHouse будет сканировать всю таблицу.
start = time.time()
result = client.query("""
    SELECT region, count(*), sum(total_amount)
    FROM sales_raw
    WHERE region = 'Москва'
    GROUP BY region
""")
end = time.time()

print(f"⏱ Время выполнения: {end - start:.2f} сек")
for row in result.result_rows:
    print(f"   Region: {row[0]}, Count: {row[1]}, Sum: {row[2]:.2f}")