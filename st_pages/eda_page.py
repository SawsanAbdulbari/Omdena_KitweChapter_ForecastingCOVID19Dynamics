import warnings
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings('ignore')


file_path = './preprocessed_data_updated.csv'

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Create a function to plot cases analysis
def plot_cases_analysis(df):
    plot_df_cases = df.groupby(['Unnamed: 0'])['imputed_total_cases'].sum().reset_index()
    fig = px.line(
        plot_df_cases,
        x='Unnamed: 0',
        y='imputed_total_cases',
        title='Total Cases Over Time',
        labels={'Unnamed: 0': 'Date', 'imputed_total_cases': 'Total Cases'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Cases', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    fig.update_layout(
        autosize=True,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

# Create a function to plot deaths analysis
def plot_deaths_analysis(df):
    plot_df_deaths = df.groupby(['Unnamed: 0'])['imputed_total_deaths'].sum().reset_index()
    fig = px.line(
        plot_df_deaths,
        x='Unnamed: 0',
        y='imputed_total_deaths',
        title='Total Deaths Over Time',
        labels={'Unnamed: 0': 'Date', 'imputed_total_deaths': 'Total Deaths'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Deaths', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    fig.update_layout(
        autosize=True,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

# Create a function to plot vaccinations analysis
def plot_vaccinations_analysis(df):
    plot_df_vaccinations = df.groupby(['Unnamed: 0'])['totalVaccinations'].sum().reset_index()
    fig = px.line(
        plot_df_vaccinations,
        x='Unnamed: 0',
        y='totalVaccinations',
        title='Total Vaccinations Over Time',
        labels={'Unnamed: 0': 'Date', 'totalVaccinations': 'Total Vaccinations'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Vaccinations', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    fig.update_layout(
        autosize=True,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main(eda):
    eda.write("<h3>📈 Exploratory Data Analysis</h3>", unsafe_allow_html=True)
    eda.write("Explore the relationship between various COVID-19 metrics by selecting from the sidebar")

    df = pd.read_csv(file_path)
    cols_0, cols_1, cols_2, cols_3 = eda.columns([1,1,1,0.5])
    
    with cols_0:
        num_filter = st.selectbox("Select a Numerical Column", [None, 'imputed_total_cases', 'imputed_total_deaths', 'totalVaccinations', 'totalTests'])
    with cols_1:
        cat_filter = st.selectbox("Select a Categorical Column", [None, 'stringency_index', 'reproduction_rate', 'rfh', 'r3h'])
    with cols_2:
        page = st.selectbox('Select a Page', ['Cases Analysis', 'Deaths Analysis', 'Vaccinations Analysis'])
    with cols_3:
        st.write("<br>", unsafe_allow_html=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name="covid_data.csv", mime="text/csv", use_container_width=True, key='eda_download')

    cols = eda.columns(2)
    with cols[0]:
        df = load_data(file_path)
        if page == 'Cases Analysis':
            st.subheader('COVID-19 Cases Analysis')
            plot_cases_analysis(df)

        elif page == 'Deaths Analysis':
            st.subheader('COVID-19 Deaths Analysis')
            plot_deaths_analysis(df)

        elif page == 'Vaccinations Analysis':
            st.subheader('COVID-19 Vaccinations Analysis')
            plot_vaccinations_analysis(df)

    with cols[1]:
        if num_filter is not None:
            fig = px.scatter(df, x=num_filter, y='totalVaccinations', color=cat_filter, size=num_filter)
            st.plotly_chart(fig, use_container_width=True)
    
    eda.dataframe(df)
    

if __name__ == '__main__':
    st.set_page_config(page_title='COVID-19 Case Prediction App', page_icon='assets/img/favicon.png', layout='wide')
    main(st)