Sales Analytics Dashboard

An interactive sales analytics dashboard built with Python and Streamlit. It turns raw sales data into KPIs, charts and auto-generated business insights, with filters for date, region and category.

🔗 Live demo: (Streamlit link yahan paste karo, deploy hone ke baad)

Features
Filters: date range, region, category
KPIs: Total Revenue, Total Profit, Orders, Profit Margin
Charts: monthly revenue and profit trend, category-wise revenue, new vs returning customers, top 10 products, region × category heatmap
Auto-generated business insights
Upload your own CSV (required columns listed below)
Download the filtered data as CSV
Tech Stack

Python, Pandas, NumPy, Plotly, Streamlit

Dataset

The app generates a synthetic dataset of 4,000 orders (Jan 2025 to Oct 2026) across 6 cities, 4 categories and 16 products, with a festive-season (Oct-Nov) sales spike built in. You can also upload your own CSV with these columns:

Order Date, Region, Category, Product, Quantity, Unit Price, Discount, Revenue, Profit, Customer Type

Key Insights

Overall: ₹2.23 crore revenue, ₹34.1 lakh profit, 15.3% profit margin across 4,000 orders.

Electronics drives revenue but not profit. It brings in about 61% of total revenue (₹1.37 crore) but runs at only a 9.2% margin.
Fashion is the margin leader. It has a 31.1% margin and earns the highest profit (₹13.7 lakh) from just 20% of revenue. Home is next at 21.4%.
Grocery is almost not worth it. Grocery has a 5.3% margin, so it adds very little profit despite many orders.
Delhi, Lucknow and Mumbai are the top 3 regions, together contributing about 62% of revenue. Delhi leads with ₹52.9 lakh.
Discounts hurt profitability badly. Orders with 20% or more discount earn a 7.8% margin, versus 17.8% for orders with no discount.
Festive season matters. October and November bring about 23% of total revenue, and October 2026 is the best month (₹20.6 lakh).
Returning customers generate about 59% of revenue, so retention is as important as acquiring new customers.
Smartphone is the top product by revenue (₹89.6 lakh), far ahead of Smartwatch and Mixer Grinder.
Business Recommendations
Push high-margin categories (Fashion, Home) through marketing and bundles.
Limit deep discounts (20%+) to slow-moving products only.
Stock up and run campaigns before October and November.
Invest in loyalty programs for returning customers.
Run Locally
pip install -r requirements.txt
python -m streamlit run app.py
Screenshots
Overview Insights Data
Author
Shashank Shekhar Singh | BCA + Data Analytics