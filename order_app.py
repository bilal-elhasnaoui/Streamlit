import streamlit as st
import pandas as pd
import plotly.express as px

# Daten einlesen
def load_data():
    file_path = "orders.csv"  # Lokaler Pfad oder hochgeladene Datei
    df = pd.read_csv(file_path)
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['ShipDate'] = pd.to_datetime(df['ShipDate'])
    return df

df = load_data()

# Streamlit App
st.title("Bestellanalysen - Interaktive Übersicht")

# Filteroptionen
regions = st.multiselect("Region auswählen", df['Region'].unique())
categories = st.multiselect("Produktkategorie auswählen", df['ProductCategory'].unique())
status = st.multiselect("Bestellstatus auswählen", df['OrderStatus'].unique())

# Daten filtern
filtered_df = df.copy()
if regions:
    filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
if categories:
    filtered_df = filtered_df[filtered_df['ProductCategory'].isin(categories)]
if status:
    filtered_df = filtered_df[filtered_df['OrderStatus'].isin(status)]

st.write("### Gefilterte Daten")
st.dataframe(filtered_df)

# Umsatz nach Region
st.write("### Umsatz nach Region")
sales_by_region = filtered_df.groupby('Region')['TotalPrice'].sum().reset_index()
fig1 = px.bar(sales_by_region, x='Region', y='TotalPrice', title="Umsatz nach Region")
st.plotly_chart(fig1)

# Umsatztrend über die Zeit
st.write("### Umsatztrend über die Zeit")
sales_trend = filtered_df.groupby('OrderDate')['TotalPrice'].sum().reset_index()
fig2 = px.line(sales_trend, x='OrderDate', y='TotalPrice', title="Umsatztrend")
st.plotly_chart(fig2)

# Bestellstatus-Verteilung
st.write("### Bestellstatus Verteilung")
fig3 = px.pie(filtered_df, names='OrderStatus', title="Bestellstatus Verteilung")
st.plotly_chart(fig3)

# Unterzahlungen analysieren
st.write("### Unterzahlungsanalyse")
underpayment_df = filtered_df[filtered_df['Underpayment'] > 0]
st.dataframe(underpayment_df[['OrderID', 'AmountPaid', 'Underpayment', 'ReasonForUnderpayment']])



