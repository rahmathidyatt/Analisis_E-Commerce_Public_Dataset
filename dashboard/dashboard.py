import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

customers_dataset = pd.read_csv ("customers_dataset.csv")
order_payments_dataset = pd.read_csv ("order_payments_dataset.csv")
orders_dataset = pd.read_csv ("orders_dataset.csv")

orders_dataset['order_purchase_timestamp'] = pd.to_datetime(orders_dataset['order_purchase_timestamp'])   

min_date = orders_dataset["order_purchase_timestamp"].min()
max_date = orders_dataset["order_purchase_timestamp"].max()
 
orders_dataset['order_purchase_timestamp'] = pd.to_datetime(orders_dataset['order_purchase_timestamp']) 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("uproject.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.header('Project Dashboard E-Commerce Dicoding :sparkles:')

#membuat diagram customer state
st.subheader("Customer State")

bystate_df = customers_dataset.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_unique_id"}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 5))  # Membuat subplot atau figur

colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_unique_id", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_unique_id", ascending=False),
    palette=colors_
)
plt.title("Number of Customer by States", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)

# Menampilkan plot di Streamlit
st.pyplot(fig)

#membuat diagram payment type
st.subheader("Payment Type")

bystate_df = order_payments_dataset.groupby(by="payment_type").order_id.nunique().reset_index()
bystate_df.rename(columns={"order_id": "payment_sequential"}, inplace=True)

plt.figure(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="payment_sequential", 
    y="payment_type",
    data=bystate_df.sort_values(by="payment_sequential", ascending=False),
    palette=colors_
)
plt.title("Payment Type", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)

# Menampilkan plot di Streamlit
st.pyplot(plt.gcf())

# Mengelompokkan data dan menghitung RFM
st.subheader("Tabel Hasil Perhitungan")
rfm_df = orders_dataset.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": lambda x: x.max(),  # Mengambil tanggal order terakhir
    "order_id": "nunique",  # Menghitung jumlah order (Frequency)
})

# Menghitung kapan terakhir pelanggan melakukan transaksi (Recency)
recent_date = rfm_df["order_purchase_timestamp"].max()
rfm_df["recency"] = (recent_date - rfm_df["order_purchase_timestamp"]).dt.days

# Menghapus kolom yang tidak diperlukan
rfm_df.drop(["order_purchase_timestamp"], axis=1, inplace=True)

# Mengubah nama kolom
rfm_df.columns = ["customer_id", "frequency", "recency"]

rfm_df.head()

# Menampilkan hasil perhitungan RFM
st.write(rfm_df)

# Buat plot
st.subheader("Diagram Hasil Perhitungan")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency", loc="center", fontsize=18)

# Memiringkan label pada sumbu x untuk subplot pertama ("By Recency")
ax[0].tick_params(axis='x', labelrotation=45, labelsize=15)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)

# Memiringkan label pada sumbu x untuk subplot kedua ("By Frequency")
ax[1].tick_params(axis='x', labelrotation=45, labelsize=15)

plt.suptitle("RFM Parameters (customer_id)", fontsize=20)

# Tampilkan plot di Streamlit
st.pyplot(fig)