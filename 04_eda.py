import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('outputs/charts', exist_ok=True)
df = pd.read_csv('outputs/superstore_clean.csv')
sns.set_theme(style='whitegrid')

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Superstore Sales Intelligence Dashboard', fontsize=16)

region_rev = df.groupby('region')['sales'].sum().reset_index()
sns.barplot(data=region_rev, x='region', y='sales',
            ax=axes[0,0], palette='Blues_d')
axes[0,0].set_title('Total Revenue by Region')
axes[0,0].set_ylabel('Revenue ($)')

cat_profit = df.groupby('category')['profit'].sum().reset_index()
sns.barplot(data=cat_profit, x='category', y='profit',
            ax=axes[0,1], palette='Greens_d')
axes[0,1].set_title('Total Profit by Category')
axes[0,1].tick_params(axis='x', rotation=15)

monthly = df.groupby(['order_year','order_month'])['sales'].sum().reset_index()
monthly['period'] = monthly['order_year'].astype(str) + '-' + monthly['order_month'].astype(str).str.zfill(2)
axes[1,0].plot(monthly['period'], monthly['sales'], color='#185FA5', linewidth=2)
axes[1,0].set_title('Monthly Revenue Trend')
axes[1,0].set_ylabel('Revenue ($)')
axes[1,0].tick_params(axis='x', rotation=90)
axes[1,0].set_xticks(axes[1,0].get_xticks()[::6])

seg_rev = df.groupby('segment')['sales'].sum().reset_index()
axes[1,1].pie(seg_rev['sales'], labels=seg_rev['segment'],
              autopct='%1.1f%%', colors=['#5DCAA5','#378ADD','#D85A30'])
axes[1,1].set_title('Revenue by Customer Segment')

plt.tight_layout()
plt.savefig('outputs/charts/sales_dashboard.png', dpi=150, bbox_inches='tight')
print("Dashboard saved!")

plt.figure(figsize=(8,5))
discount_profit = df.groupby('discount')['profit'].mean().reset_index()
plt.plot(discount_profit['discount'], discount_profit['profit'],
         color='#D85A30', linewidth=2, marker='o', markersize=4)
plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
plt.title('Impact of Discount on Average Profit')
plt.xlabel('Discount Rate')
plt.ylabel('Average Profit ($)')
plt.tight_layout()
plt.savefig('outputs/charts/discount_impact.png', dpi=150, bbox_inches='tight')
print("Discount impact chart saved!")
print("\nAll charts saved to outputs/charts/")