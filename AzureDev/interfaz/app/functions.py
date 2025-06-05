import streamlit as st
import pandas as pd
import plotly.graph_objects as go


## Navigation functions
def go_to_page(name):
    '''
    Function to navigate to a different page in the Streamlit app.
    '''  
    st.session_state.page = name
    st.experimental_rerun()


## Other functions
def kpi_data(data, profile):
    '''
    Function to extract data from the most recent month and the previous month for a given profile.
    '''
    if profile not in data['Profile'].unique():
        filtered_data = data
    else:
        filtered_data = data[data['Profile'] == profile]
    
    # Get latest month and previous month
    most_recent_month = data['CreatedOn'].max()
    previous_month = most_recent_month - pd.DateOffset(months=1)
    most_recent_month = most_recent_month.strftime('%Y-%m')
    previous_month = previous_month.strftime('%Y-%m')

    # Filter data for the most recent and previous months
    current_data = filtered_data[filtered_data['GraphDate'] == most_recent_month]
    previous_data = filtered_data[filtered_data['GraphDate'] == previous_month]

    return current_data, previous_data

# KPI functions
def average_rate(data, profile):
    '''
    Function to calculate the average rate for a given month and profile.
    '''
    current_data, previous_data = kpi_data(data, profile)

    if current_data.empty or previous_data.empty:
        return 0.0
    
    dar_current = current_data['USDAmount'].sum() / current_data['RegId'].nunique()
    dar_previous = previous_data['USDAmount'].sum() / previous_data['RegId'].nunique()
    
    return dar_current, dar_previous


def average_los(data, profile):
    '''
    Function to calculate the average length of stay for a given month and profile.
    '''
    current_data, previous_data = kpi_data(data, profile)
    
    if current_data.empty or previous_data.empty:
        return 0.0

    los_current = current_data['Nights'].sum() / current_data['RegId'].nunique()
    los_previous = previous_data['Nights'].sum() / previous_data['RegId'].nunique()
    
    return los_current, los_previous


def kpi_reservations(data, profile):
    '''
    Function to calculate the number of reservations per month for a given profile.
    '''
    if profile not in data['Profile'].unique():
        filtered_data = data
    else:
        filtered_data = data[data['Profile'] == profile]
    
    # Get latest month and previous month
    most_recent_month = data['CreatedOn'].max()
    previous_month = most_recent_month - pd.DateOffset(months=1)
    most_recent_month = most_recent_month.strftime('%Y-%m')
    previous_month = previous_month.strftime('%Y-%m')

    # Group by month and count unique reservations
    monthly_reservations = filtered_data.groupby('GraphDate')['RegId'].nunique().reset_index()
    current_reservations = monthly_reservations[monthly_reservations['RegId'] == most_recent_month]['RegId'].nunique()
    previous_reservations = monthly_reservations[monthly_reservations['GraphDate'] == previous_month]['RegId'].nunique()
    
    return current_reservations, previous_reservations


def kpi_revenue(data, profile):
    '''
    Function to calculate the total revenue for a given month and profile.
    '''
    current_data, previous_data = kpi_data(data, profile)
    
    if current_data.empty or previous_data.empty:
        return 0.0
    
    revenue_current = current_data['USDAmount'].sum()
    revenue_previous = previous_data['USDAmount'].sum()
    
    return revenue_current, revenue_previous


## Graphing functions
def plot_bar_chart(data, client, type):
    # Filter data for the specified profile
    if client in data['Profile'].unique():
        label_data = data[data['Profile'] == client]
    else:
        label_data = data

    fig = go.Figure()
    monthly_label_data = label_data.groupby('GraphDate').agg({'RegId': 'nunique', 'USDAmount': 'sum'}).reset_index()
    monthly_label_data['GraphDate'] = monthly_label_data['GraphDate'].dt.to_timestamp()
    monthly_label_data.rename(columns={'RegId': 'Number of Clients', 'USDAmount': 'USDAmount'}, inplace=True)
    if type == 'clients':
        fig.add_trace(go.Scatter(x=monthly_label_data['GraphDate'], y=monthly_label_data['Number of Clients'], mode='lines+markers', name=f'Clients {client}'))
        fig.update_layout(
            title='Monthly Number of Clients',
            xaxis_title='Date',
            yaxis_title='Number of Clients',
            yaxis2=dict(title='Revenue', overlaying='y', side='right'),
            template='plotly_white')
        
    elif type == 'revenue':
        fig.add_trace(go.Scatter(x=monthly_label_data['GraphDate'], y=monthly_label_data['USDAmount'], mode='lines+markers', name=f'Revenue {client}', yaxis='y2'))
        fig.update_layout(
            title='Monthly Revenue in USD',
            xaxis_title='Date',
            yaxis_title='Number of Clients',
            yaxis2=dict(title='Revenue', overlaying='y', side='right'),
            template='plotly_white')

    # Return the figure object    
    return fig
    
# Styling functions
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)