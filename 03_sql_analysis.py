import pandas as pd
import sqlite3
import os

os.makedirs('outputs', exist_ok=True)
df = pd.read_csv('outputs/superstore_clean.csv')

conn = sqlite3.connect(':memory:')
df.to_sql('superstore', conn, index=False, if_exists='replace')

queries = {
    "revenue_by_region": """
        SELECT region,
               COUNT(*) as total_orders,
               ROUND(SUM(sales), 2) as total_revenue,
               ROUND(SUM(profit), 2) as total_profit,
               ROUND(AVG(profit_margin), 2) as avg_profit_margin
        FROM superstore
        GROUP BY region
        ORDER BY total_revenue DESC
    """,
    "top_performing_categories": """
        SELECT category,
               "sub-category",
               COUNT(*) as orders,
               ROUND(SUM(sales), 2) as revenue,
               ROUND(SUM(profit), 2) as profit,
               ROUND(AVG(profit_margin), 2) as avg_margin
        FROM superstore
       GROUP BY category, "sub-category"
        ORDER BY profit DESC
        LIMIT 10
    """,
    "monthly_revenue_trend": """
        SELECT order_year,
               order_month,
               COUNT(*) as orders,
               ROUND(SUM(sales), 2) as monthly_revenue,
               ROUND(SUM(profit), 2) as monthly_profit
        FROM superstore
        GROUP BY order_year, order_month
        ORDER BY order_year, order_month
    """,
    "shipping_performance": """
        SELECT ship_mode,
               COUNT(*) as total_orders,
               ROUND(AVG(shipping_days), 1) as avg_shipping_days,
               ROUND(SUM(sales), 2) as total_revenue,
               ROUND(AVG(discount), 2) as avg_discount
        FROM superstore
        GROUP BY ship_mode
        ORDER BY avg_shipping_days
    """,
    "customer_segment_analysis": """
        SELECT segment,
               COUNT(DISTINCT customer_id) as unique_customers,
               COUNT(*) as total_orders,
               ROUND(SUM(sales), 2) as total_revenue,
               ROUND(AVG(sales), 2) as avg_order_value,
               ROUND(SUM(profit), 2) as total_profit
        FROM superstore
        GROUP BY segment
        ORDER BY total_revenue DESC
    """,
    "loss_making_products": """
        SELECT product_name,
               category,
               COUNT(*) as times_ordered,
               ROUND(SUM(sales), 2) as total_revenue,
               ROUND(SUM(profit), 2) as total_loss,
               ROUND(AVG(discount), 2) as avg_discount
        FROM superstore
        WHERE profit < 0
        GROUP BY product_name, category
        ORDER BY total_loss ASC
        LIMIT 10
    """
}

for name, query in queries.items():
    result = pd.read_sql_query(query, conn)
    result.to_csv(f'outputs/sql_{name}.csv', index=False)
    print(f"\n=== {name.upper()} ===")
    print(result.to_string(index=False))

conn.close()
print("\n=== ALL SQL QUERIES DONE ===")
print("Results saved to /outputs folder")