import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page configuration

data = pd.read_csv("interfaz/app/datafeik.csv")
data['RegId'] = data['Profile_id'].astype(str) + data['Reservation_clave'] + data['CreatedOn'].astype(str)
data['CreatedOn'] = pd.to_datetime(data['CreatedOn'])
data['Datestart'] = pd.to_datetime(data['Datestart'])
data['Dateend'] = pd.to_datetime(data['Dateend'])
data['GraphDate'] = data['Datestart'].dt.to_period('M')

st.title("Dashboard Interactivo de Clientes")

# Sidebar para selección de variables y tipo de gráfico
st.sidebar.header("Opciones de visualización")

# Selección de variables numéricas y categóricas
num_vars = data.select_dtypes(include=['number']).columns.tolist()
cat_vars = data.select_dtypes(include=['object', 'category']).columns.tolist()

x_var = st.sidebar.selectbox("Variable en el eje X", options=num_vars + cat_vars, index=0)
y_var = st.sidebar.selectbox("Variable en el eje Y", options=[None] + num_vars, index=0)
graph_type = st.sidebar.selectbox("Tipo de gráfico", options=["Histograma", "Barras", "Dispersión", "Boxplot"])

# Filtros interactivos para variables categóricas
st.sidebar.header("Filtros")
filters = {}
for col in cat_vars:
    unique_vals = data[col].dropna().unique().tolist()
    if len(unique_vals) > 1 and len(unique_vals) < 30:
        selected = st.sidebar.multiselect(f"Filtrar {col}", unique_vals, default=unique_vals)
        filters[col] = selected

# Aplicar filtros
filtered_data = data.copy()
for col, vals in filters.items():
    filtered_data = filtered_data[filtered_data[col].isin(vals)]

# Mostrar gráfico según selección
st.subheader(f"Visualización: {graph_type}")
if graph_type == "Histograma":
    st.plotly_chart(px.histogram(filtered_data, x=x_var), use_container_width=True)
elif graph_type == "Barras":
    st.plotly_chart(px.bar(filtered_data, x=x_var, y=y_var) if y_var else px.bar(filtered_data, x=x_var), use_container_width=True)
elif graph_type == "Dispersión":
    if y_var:
        st.plotly_chart(px.scatter(filtered_data, x=x_var, y=y_var), use_container_width=True)
    else:
        st.info("Selecciona una variable para el eje Y.")
elif graph_type == "Boxplot":
    if y_var:
        st.plotly_chart(px.box(filtered_data, x=x_var, y=y_var), use_container_width=True)
    else:
        st.info("Selecciona una variable para el eje Y.")

st.dataframe(filtered_data.head(100))
