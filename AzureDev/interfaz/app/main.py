import streamlit as st
from time import sleep

st.set_page_config(page_title="TCA ClientProfiler", page_icon=":busts_in_silhouette:", layout="wide")

# Login setup
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Login
if not st.session_state.logged_in:
    placeholder = st.empty()

    with placeholder.form("login"):
        # Restrict the width of the header image
        st.image("interfaz/images/tca_header.jpeg")
        st.markdown("<h1 style='text-align: center;'>TCA ClientProfiler</h1>", unsafe_allow_html=True)
        st.markdown("### Iniciar sesión")
        username = st.text_input("Usuario", placeholder="Ingresa tu usuario")
        password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
        submit = st.form_submit_button("Iniciar sesión")

    if submit:
        if (username == "admin" and password == "admin") or (username == "user" and password == "user"):
            st.session_state.logged_in = True
            st.session_state.username = username
            placeholder.empty()
            st.success(f"Inicio de sesión exitoso para {username.upper()}")
            sleep(1)
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


pages = {
    "Navegación": [
        st.Page("inicio.py", title="Inicio"),
        st.Page("dashboard.py", title="Visualizaciones"),
        st.Page("admin.py", title="Modificar datos"),
    ]
}

if st.session_state.logged_in:
    pg = st.navigation(pages, position="hidden")
    pg.run()