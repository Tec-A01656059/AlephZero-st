import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from functions import plot_bar_chart
import clasificador

# CSS styling
with open("interfaz/app/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data
data = pd.read_csv("interfaz/app/GH_DataHistory.csv")

b1, b2 = st.columns([0.9, 0.07])
b1.empty()
if b2.button("⬅ Volver"):
    st.switch_page("inicio.py")

# Upload new clients
t1,t2 = st.columns([0.4, 0.9])
key_date = t1.date_input("Selecciona mes de reporte", value=pd.to_datetime("2020-01-01"), key="report_date")
key_date = pd.to_datetime(key_date)
key_date = key_date.to_period('M')

new_data = t2.file_uploader("Cargar archivo CSV", type=["csv"])


if new_data is not None:
    # Read the uploaded CSV file
    clientes_noclasificados = pd.read_csv(new_data)

    # Get assigned cluster
    clasificar = clasificador.GuestProfileClassifier('interfaz/app/model.pkl')
    clusters = clasificar.classify(clientes_noclasificados, muestra=len(clientes_noclasificados))
    clientes_noclasificados['cluster'] = clusters
    clientes_noclasificados['Profile'] = clientes_noclasificados['cluster'].map({0: 'A', 1: 'B', 2: 'C'})
    clientes_noclasificados['GraphDate'] = [key_date for _ in range(len(clientes_noclasificados))]

    # Show the dataframe with assigned profiles
    st.subheader("Clasificación de clientes")
    st.dataframe(clientes_noclasificados[['Profile', 'Adults', 'Minors', 'FreeMinors', 'Nights', 'LocalCurrencyAmount']])

    clientes_noclasificados_mod = clientes_noclasificados.copy()
    clientes_noclasificados_mod['RegId'] = random.sample(range(100000, 999999), len(clientes_noclasificados_mod))

    c1,c2 = st.columns([0.9, 0.9])

    # Pie chart for profile distribution
    with c1.container():
        profile_counts = data['Profile'].value_counts()
        pie = go.Figure(data=[go.Pie(labels=profile_counts.index, values=profile_counts.values)])
        pie.update_layout(title_text='Distribución de Perfiles de Clientes')
        st.plotly_chart(pie, use_container_width=True)

    # Monthly KPIs
    with c2.container():
        m2, m3 = st.columns(2)
        m2.metric(label="Total de clientes:", value=clientes_noclasificados_mod['RegId'].nunique())
        m3.metric(label="Ingresos totales:", value=f"${clientes_noclasificados_mod['LocalCurrencyAmount'].sum():,.2f}")

        # Create a line plot for the number of clients
        m2.plotly_chart(plot_bar_chart(clientes_noclasificados_mod, 'all', 'clients'), use_container_width=True)
            
        # Create a line plot for the revenue
        m3.plotly_chart(plot_bar_chart(clientes_noclasificados_mod, 'all', 'revenue'), use_container_width=True)
