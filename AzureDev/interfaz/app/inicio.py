import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px
import plotly.graph_objects as go
from functions import go_to_page, plot_bar_chart, average_rate, average_los, kpi_reservations, kpi_revenue

# CSS styling
with open("interfaz/app/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

## Functions
def basic_layout(profile):
    b1,b2, = st.columns([0.27, 0.9])

    if profile not in data['Profile'].unique():
        filtered_df = data
    else:
        filtered_df = data[data['Profile'] == profile]
    
    profile_facts = profile_data[profile_data['Profile'] == profile]
    
    b1.image(f'interfaz/images/cluster{profile}.jpg')
    with b1.container(border=True):
        st.write("##### Características del perfil:")
        st.write(f'- Adulto(s): {int(np.ceil(profile_facts["Adults"].values[0])):2d}')
        st.write(f'- Menor(es) mayores de 3 años: {int(np.ceil(profile_facts["Minors"].values[0])):2d}')
        st.write(f'- Menor(es) menores de 3 años: {int(np.ceil(profile_facts["FreeMinors"].values[0])):2d}')
        st.write(f'- Estancia promedio: {profile_facts["Nights"].values[0]} noches')
        st.write(f'- Tarifa promedio: {profile_facts["LocalCurrencyAmount"].values[0]} USD')
    
    with b2.container():
        
        st.markdown("<h2 style='text-align: center;'>KPIs Principales</h2>", unsafe_allow_html=True)
        k1,k2,k3,k4 = st.columns([0.95, 0.95, 0.95, 0.95])

        adr_actual, adr_anterior = average_rate(filtered_df, profile)
        k1.metric(
            label="Tarifa promedio por reservación (ADR)", 
            value=f'{adr_actual:.2f} USD',
            delta = f"{adr_actual - adr_anterior:.2f} USD respecto al mes anterior")
        
        los_actual, los_anterior = average_los(filtered_df, profile)
        k2.metric(
            label="Longitud de estancia promedio (LOS)", 
            value=f'{los_actual:.2f} noches',
            delta = f"{los_actual - los_anterior:.2f} noches respecto al mes anterior")
        
        res_actual, res_anterior = kpi_reservations(filtered_df, profile)
        k3.metric(
            label="Total de reservaciones",
            value=f"{res_actual} reservaciones",
            delta=f"{res_actual - res_anterior} respecto al mes anterior")
        
        ing_actual, ing_anterior = kpi_revenue(filtered_df, profile)
        k4.metric(
            label="Ingresos totales",
            value=f"${ing_actual:,.2f} USD",
            delta=f"${ing_actual - ing_anterior:.2f} respecto al mes anterior"
        )
        
        m2,m3 = st.columns([0.95, 0.95])
        # Create a line plot for the number of clients
        m2.plotly_chart(plot_bar_chart(filtered_df, profile, 'clients'), use_container_width=True)
        
        # Create a line plot for the revenue
        m3.plotly_chart(plot_bar_chart(filtered_df, profile, 'revenue'), use_container_width=True)

    with b2.expander("Estrategias de marketing", expanded=False):
        st.write("Pregúntale a alguien de merca bro")

random.seed(42)  # For reproducibility

# Streamlit app setup
if "page" not in st.session_state or st.session_state.page not in ["inicio", "A", "B", "C"]:
    st.session_state.page = "inicio"


with st.spinner('Updating report...'):
    # Data processing
    profile_data = pd.read_csv("interfaz/app/profiles.csv")
    data = pd.read_csv("interfaz/app/GH_DataHistory.csv")
    # Convert YYYY-MM to datetime and create a period for graphing
    data['GraphDate'] = pd.to_datetime(data['GraphDate']).dt.to_period('M')
    # Create a unique identifier for each reservation
    data['RegId'] = random.sample(range(100000, 999999), len(data))
    
    ## Gallery Section
    if st.session_state.page == "inicio":
        st.image("interfaz/images/tca_header2.jpeg")
        
        ## Header Section
        t1,t2 = st.columns([0.6, 0.2])
        
        t1.markdown("<h1 style='text-align: center;'>TCA ClientProfiler</h1>", unsafe_allow_html=True)
        #t1.title("TCA ClientProfiler")
        t1.markdown("Descubre los perfiles de tus clientes y optimiza tus estrategias de negocio con decisiones informadas: analiza comportamientos, identifica tendencias y maximiza tus ingresos.")

        if st.session_state.username == 'admin':
            if t2.button("Modificar datos"):
                st.switch_page("admin.py")
                st.rerun()
        
        if t2.button("Más visualizaciones"):
            st.switch_page("dashboard.py")
            st.rerun()
        
        if t2.button("Clasificar reservación"):
            go_to_page("clasificar")
            st.rerun()

        
        g1,g2,g3 = st.columns([0.7, 0.7, 0.5])

        ## General Visualizations
        fig1 = go.Figure()
        grouped_data = data.groupby(['GraphDate', 'Profile']).agg({'RegId':'nunique'}).reset_index()
        grouped_data['GraphDate'] = grouped_data['GraphDate'].dt.to_timestamp()

        # Stacked bar chart for revenue per month
        fig1 = px.bar(
            grouped_data,
            x='GraphDate',
            y='RegId',
            color='Profile',
            title='Total de clientes por perfil',
            barmode='stack',
            labels={'GraphDate': 'Fecha', 'RegId': 'Recuento'},
            template='plotly_white'
        )
        fig1.update_layout(
            xaxis_title='Fecha',
            yaxis_title='Recuento',
            barmode='stack',
            xaxis=dict(tickformat='%Y-%m')
        )
        g1.plotly_chart(fig1, use_container_width=True)


        fig2 = go.Figure()
        grouped_data = data.groupby(['GraphDate', 'Profile']).agg({'LocalCurrencyAmount': 'sum'}).reset_index()
        grouped_data['GraphDate'] = grouped_data['GraphDate'].dt.to_timestamp()

        # Stacked bar chart for revenue per month
        fig2 = px.bar(
            grouped_data,
            x='GraphDate',
            y='LocalCurrencyAmount',
            color='Profile',
            title='Ingreso mensual por perfil',
            barmode='stack',
            labels={'GraphDate': 'Fecha', 'LocalCurrencyAmount': 'Ingresos'},
            template='plotly_white'
        )
        fig2.update_layout(
            xaxis_title='Fecha',
            yaxis_title='Ingresos',
            barmode='stack',
            xaxis=dict(tickformat='%Y-%m')
        )
        g2.plotly_chart(fig2, use_container_width=True)


        g3.write("### KPIs principales")

        adr_actual, adr_anterior = average_rate(data, 'all')
        g3.metric(
            label="Tarifa promedio por reservación (ADR)", 
            value=f'{adr_actual:.2f} USD',
            delta = f"{adr_actual - adr_anterior:.2f} USD respecto al mes anterior")
        
        los_actual, los_anterior = average_los(data, 'all')
        g3.metric(
            label="Longitud de estancia promedio (LOS)", 
            value=f'{los_actual:.2f} noches',
            delta = f"{los_actual - los_anterior:.2f} noches respecto al mes anterior")
        
        res_actual, res_anterior = kpi_reservations(data, 'all')
        g3.metric(
            label="Total de reservaciones",
            value=f"{res_actual} reservaciones",
            delta=f"{res_actual - res_anterior} respecto al mes anterior")
        
        ing_actual, ing_anterior = kpi_revenue(data, 'all')
        g3.metric(
            label="Ingresos totales",
            value=f"${ing_actual:,.2f} USD",
            delta=f"${ing_actual - ing_anterior:.2f} respecto al mes anterior"
        )
        
        st.markdown("## Tus principales perfiles de clientes:")
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container():
                st.image("interfaz/images/clusterA.jpg")
                st.markdown("### Viajeros Individuales")
                if st.button("Más información", key="perfil1"):
                    go_to_page("A")
                    st.rerun()

        with col2:
            with st.container():
                st.image("interfaz/images/clusterB.jpg")
                st.markdown("### Parejas sin menores")
                if st.button("Más información", key="perfil2"):
                    go_to_page("B")
                    st.rerun()
        
        with col3:
            with st.container():
                st.image("interfaz/images/clusterC.jpg")
                st.markdown("### Familias")
                if st.button("Más información", key="perfil3"):
                    go_to_page("C")
                    st.rerun()


    elif st.session_state.page == "A":
        st.title("Perfil 1: Viajeros Individuales")
        basic_layout(profile='A')
        if st.button("⬅ Volver"):
            go_to_page("inicio")

    elif st.session_state.page == "B":
        st.title("Perfil 2: Parejas sin menores")
        basic_layout(profile='B')
        if st.button("⬅ Volver"):
            go_to_page("inicio")

    elif st.session_state.page == "C":
        st.title("Perfil 3: Familias")
        basic_layout(profile='C')
        if st.button("⬅ Volver"):
            go_to_page("inicio")