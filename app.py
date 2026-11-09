import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

REQUIRED = ["Order Date", "Region", "Category", "Product", "Quantity",
            "Unit Price", "Discount", "Revenue", "Profit", "Customer Type"]




@st.cache_data
def generate_data(n=4000, seed=42):
    """Sample sales data banata hai, taaki dataset download na karna pade."""
    rng = np.random.default_rng(seed)
    catalog = {
        "Electronics": {"Smartphone": 15000, "Headphones": 2000, "Smartwatch": 5000, "Power Bank": 1200},
        "Fashion": {"T-Shirt": 600, "Jeans": 1800, "Sneakers": 2500, "Jacket": 3000},
        "Grocery": {"Rice 5kg": 450, "Cooking Oil": 180, "Tea Pack": 250, "Snacks Combo": 300},
        "Home": {"Mixer Grinder": 3500, "Bedsheet": 900, "Table Lamp": 700, "Water Bottle": 350},
    }
    margin = {"Electronics": 0.12, "Fashion": 0.35, "Grocery": 0.08, "Home": 0.25}
    regions = ["Lucknow", "Delhi", "Mumbai", "Kanpur", "Varanasi", "Bengaluru"]
    region_w = [0.22, 0.24, 0.20, 0.10, 0.08, 0.16]

    dates = pd.date_range("2025-01-01", "2026-10-31")
    # Festive season (Oct-Nov) mein zyada sales
    weights = np.where(dates.month.isin([10, 11]), 2.0, 1.0)
    weights = weights / weights.sum()

    rows = []
    for _ in range(n):
        cat = rng.choice(list(catalog))
        prod = rng.choice(list(catalog[cat]))
        price = catalog[cat][prod]
        qty = int(rng.integers(1, 5))
        disc = float(rng.choice([0, 0.05, 0.10, 0.20], p=[0.5, 0.2, 0.2, 0.1]))
        revenue = qty * price * (1 - disc)
        profit = revenue * (margin[cat] - disc / 2) * rng.uniform(0.8, 1.1)
        rows.append({
            "Order Date": rng.choice(dates, p=weights),
            "Region": rng.choice(regions, p=region_w),
            "Category": cat,
            "Product": prod,
            "Quantity": qty,
            "Unit Price": price,
            "Discount": disc,
            "Revenue": round(revenue, 2),
            "Profit": round(profit, 2),
            "Customer Type": rng.choice(["New", "Returning"], p=[0.4, 0.6]),
        })
    return pd.DataFrame(rows)


def inr(x):
    return f"₹{x:,.0f}"




# ---------- Sidebar ----------
st.sidebar.title("🔎 Filters")
uploaded = st.sidebar.file_uploader("Apni CSV upload karo (optional)", type="csv")

df = generate_data()
if uploaded is not None:
    user_df = pd.read_csv(uploaded)
    missing = [c for c in REQUIRED if c not in user_df.columns]
    if missing:
        st.sidebar.error(f"Ye columns missing hain: {', '.join(missing)}")
    else:
        user_df["Order Date"] = pd.to_datetime(user_df["Order Date"])
        df = user_df

min_d, max_d = df["Order Date"].min().date(), df["Order Date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
start, end = date_range if len(date_range) == 2 else (min_d, max_d)

regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))

mask = (
    (df["Order Date"].dt.date >= start)
    & (df["Order Date"].dt.date <= end)
    & df["Region"].isin(regions)
    & df["Category"].isin(cats)
)
data = df[mask].copy()




# ---------- Header ----------
st.title("📊 Sales Analytics Dashboard")
st.caption("Python + Pandas + Plotly + Streamlit se bana end-to-end analytics project")

if data.empty:
    st.warning("Selected filters mein koi data nahi hai. Filters change karo.")
    st.stop()

# ---------- KPIs ----------
revenue, profit, orders = data["Revenue"].sum(), data["Profit"].sum(), len(data)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", inr(revenue))
c2.metric("Total Profit", inr(profit))
c3.metric("Orders", f"{orders:,}")
c4.metric("Profit Margin", f"{profit / revenue * 100:.1f}%")

data["Month"] = data["Order Date"].dt.to_period("M").dt.to_timestamp()
monthly = data.groupby("Month", as_index=False)[["Revenue", "Profit"]].sum()

tab1, tab2, tab3 = st.tabs(["📈 Overview", "💡 Insights", "🗂️ Data"])




# ---------- Overview ----------
with tab1:
    st.subheader("Monthly Revenue & Profit")
    st.plotly_chart(px.line(monthly, x="Month", y=["Revenue", "Profit"], markers=True))

    left, right = st.columns(2)
    with left:
        st.subheader("Category-wise Revenue")
        cat_df = data.groupby("Category", as_index=False)["Revenue"].sum()
        st.plotly_chart(px.bar(cat_df, x="Category", y="Revenue", color="Category"))
    with right:
        st.subheader("New vs Returning Customers")
        cust_df = data.groupby("Customer Type", as_index=False)["Revenue"].sum()
        st.plotly_chart(px.pie(cust_df, names="Customer Type", values="Revenue", hole=0.45))

    left, right = st.columns(2)
    with left:
        st.subheader("Top 10 Products")
        top = data.groupby("Product")["Revenue"].sum().nlargest(10).reset_index()
        fig = px.bar(top, x="Revenue", y="Product", orientation="h")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig)
    with right:
        st.subheader("Region × Category Heatmap")
        pivot = data.pivot_table(index="Region", columns="Category", values="Revenue", aggfunc="sum", fill_value=0)
        st.plotly_chart(px.imshow(pivot, text_auto=".2s", aspect="auto", color_continuous_scale="Blues"))


        

# ---------- Insights ----------
with tab2:
    st.subheader("Auto-generated Insights")
    best_region = data.groupby("Region")["Revenue"].sum().idxmax()
    best_cat = data.groupby("Category")["Revenue"].sum().idxmax()
    best_margin_cat = (data.groupby("Category")["Profit"].sum() / data.groupby("Category")["Revenue"].sum()).idxmax()
    best_month = monthly.loc[monthly["Revenue"].idxmax()]
    disc_high = data[data["Discount"] >= 0.20]["Profit"].sum() / max(data[data["Discount"] >= 0.20]["Revenue"].sum(), 1)
    disc_none = data[data["Discount"] == 0]["Profit"].sum() / max(data[data["Discount"] == 0]["Revenue"].sum(), 1)

    st.markdown(f"""
- 🏆 **Sabse zyada revenue wala region:** {best_region}
- 🛒 **Top category (revenue):** {best_cat}
- 💰 **Sabse high margin category:** {best_margin_cat}
- 📅 **Best month:** {best_month['Month']:%B %Y} ({inr(best_month['Revenue'])})
- 🏷️ **Discount impact:** 20%+ discount par margin {disc_high*100:.1f}% hai, jabki bina discount ke {disc_none*100:.1f}%
- 🔁 **Returning customers ka revenue share:** {data[data['Customer Type']=='Returning']['Revenue'].sum() / revenue * 100:.1f}%
""")
    st.info("Business suggestion: High-margin categories ko promote karo aur zyada discount sirf slow-moving products par do.")


    
# ---------- Data ----------
with tab3:
    st.subheader("Filtered Data (pehli 100 rows)")
    show = data.drop(columns="Month")
    html_table = show.head(100).to_html(index=False)
    st.markdown(f'<div style="overflow-x:auto">{html_table}</div>', unsafe_allow_html=True)
    st.download_button("⬇️ Download filtered CSV", show.to_csv(index=False).encode("utf-8"),
                       "filtered_sales.csv", "text/csv")