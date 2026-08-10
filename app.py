import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Retail Store Sales Analysis",
    page_icon="📊",
    layout="wide"
)



@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_store_sales.csv")
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
    return df


df = load_data()


st.title("📊 Retail Store Sales Analysis")
st.write(
    "Interactive dashboard for exploring retail sales performance, "
    "products, categories, locations, payment methods, and discounts."
)



total_sales = df["Total Spent"].sum()
total_transactions = df["Transaction ID"].nunique()
total_customers = df["Customer ID"].nunique()
total_quantity = df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Transactions", f"{total_transactions:,}")
col3.metric("Customers", f"{total_customers:,}")
col4.metric("Quantity Sold", f"{total_quantity:,}")


st.divider()



st.subheader("Sales by Category")

category_sales = (
    df.groupby("Category")["Total Spent"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))
category_sales.plot(kind="bar", ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Total Sales")
ax.set_title("Total Sales by Category")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)



st.subheader("Sales by Location")

location_sales = (
    df.groupby("Location")["Total Spent"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(7, 4))
location_sales.plot(kind="bar", ax=ax)
ax.set_xlabel("Location")
ax.set_ylabel("Total Sales")
ax.set_title("Online vs In-store Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)



st.subheader("Payment Methods")

payment_counts = df["Payment Method"].value_counts()

fig, ax = plt.subplots(figsize=(7, 4))
payment_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Payment Method")
ax.set_ylabel("Number of Transactions")
ax.set_title("Transactions by Payment Method")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

st.subheader("Yearly Sales")

df["Year"] = df["Transaction Date"].dt.year

yearly_sales = (
    df.groupby("Year")["Total Spent"]
    .sum()
)

fig, ax = plt.subplots(figsize=(9, 4))
yearly_sales.plot(kind="line", marker="o", ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Total Sales")
ax.set_title("Sales Trend by Year")
ax.grid(True)

st.pyplot(fig)

st.subheader("Top 10 Known Items")

known_items = df[df["Item"] != "Unknown"]

item_sales = (
    known_items.groupby("Item")["Total Spent"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(item_sales.reset_index(), use_container_width=True)


st.subheader("Discount Analysis")

discount_counts = (
    df["Discount Applied"]
    .value_counts(dropna=False)
)

st.dataframe(
    discount_counts.rename("Count").reset_index(),
    use_container_width=True
)


st.subheader("🔎 Key Insights")

top_category = category_sales.idxmax()
top_category_sales = category_sales.max()

top_location = location_sales.idxmax()
top_location_sales = location_sales.max()

top_payment = payment_counts.idxmax()
top_payment_count = payment_counts.max()

best_year = yearly_sales.idxmax()
best_year_sales = yearly_sales.max()

st.write(f"🏆 **Top Category:** {top_category} — {top_category_sales:,.0f}")
st.write(f"🌐 **Top Location:** {top_location} — {top_location_sales:,.0f}")
st.write(f"💳 **Most Used Payment Method:** {top_payment} — {top_payment_count:,} transactions")
st.write(f"📅 **Best Year:** {best_year} — {best_year_sales:,.0f}")