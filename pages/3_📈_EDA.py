import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.title(":chart_with_upwards_trend: Exploratory Data Analysis")

# Load the dataset
file_path = './data/preprocessed_data_updated.csv'
df = pd.read_csv(file_path)

# Sidebar for additional information
st.sidebar.title('COVID-19 Dashboard')
st.sidebar.image("./media/omdena_zambia_highres.png", use_column_width='always') 
st.sidebar.write("This dashboard provides an overview of COVID-19 data, including cases, deaths, vaccinations, and testing trends.")
st.sidebar.divider()


# Set page title and description
st.subheader("Exploratory Data Analysis")
st.write("Explore the relationship between various COVID-19 metrics by selecting from the sidebar")

# Sidebar with filters
st.sidebar.header("Filters:")
num_filter = st.sidebar.selectbox("Select a Numerical Column", [None, 'imputed_total_cases', 'imputed_total_deaths', 'totalVaccinations', 'totalTests'])
cat_filter = st.sidebar.selectbox("Select a Categorical Column", [None, 'stringency_index', 'reproduction_rate', 'rfh', 'r3h'])

if num_filter is not None:
    fig = px.scatter(df, x=num_filter, y='totalVaccinations', color=cat_filter, size=num_filter)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("View Data"):
    st.write(df.iloc[:500].style.background_gradient(cmap="Oranges"))

# Download the filtered DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="covid_data.csv", mime="text/csv")


@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    return df

# Define the main function
def main():
    df = load_data()

    # Create a sidebar for page navigation
    page = st.sidebar.selectbox('Select a Page', ['Cases Analysis', 'Deaths Analysis', 'Vaccinations Analysis'])

    if page == 'Cases Analysis':
        st.subheader('COVID-19 Cases Analysis')
        plot_cases_analysis(df)

    elif page == 'Deaths Analysis':
        st.subheader('COVID-19 Deaths Analysis')
        plot_deaths_analysis(df)
        plot_total_recovery_analysis(df)

    elif page == 'Vaccinations Analysis':
        st.subheader('COVID-19 Vaccinations Analysis')
        plot_vaccinations_analysis(df)

# Create a function to plot cases analysis
def plot_cases_analysis(df):
    plot_df_cases = df.groupby(['Unnamed: 0'])['imputed_total_cases'].sum().reset_index()
    fig = px.line(
        plot_df_cases,
        x='Unnamed: 0',
        y='imputed_total_cases',
        title='Total Cases Over Time',
        labels={'Unnamed: 0': '', 'imputed_total_cases': 'Total Cases'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Cases', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

# Create a function to plot deaths analysis
def plot_deaths_analysis(df):
    plot_df_deaths = df.groupby(['Unnamed: 0'])['imputed_total_deaths'].sum().reset_index()
    fig = px.line(
        plot_df_deaths,
        x='Unnamed: 0',
        y='imputed_total_deaths',
        title='Total Deaths Over Time',
        labels={'Unnamed: 0': '', 'imputed_total_deaths': 'Total Deaths'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Deaths', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

#Create a function to plot recovery rate over time 
def plot_total_recovery_analysis(df):
    plot_df_recovery = df.groupby(['Unnamed: 0'])['imputed_total_recoveries'].sum().reset_index()
    fig = px.scatter(
        plot_df_recovery,
        x='Unnamed: 0',
        y='imputed_total_recoveries',
        title='Total recovery over Time',
        labels={'Unnamed: 0': '', 'imputed_total_recoveries': 'Recovery Rate'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Recovery Rate', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)    

# Create a function to plot vaccinations analysis
def plot_vaccinations_analysis(df):
    plot_df_vaccinations = df.groupby(['Unnamed: 0'])['totalVaccinations'].sum().reset_index()
    fig = px.line(
        plot_df_vaccinations,
        x='Unnamed: 0',
        y='totalVaccinations',
        title='Total Vaccinations Over Time',
        labels={'Unnamed: 0': '', 'totalVaccinations': 'Total Vaccinations'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Vaccinations', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)
# Define the main function
def main():
    df = load_data()

    # Create a sidebar for page navigation
    page = st.sidebar.selectbox('Select a Page', ['Cases Analysis', 'Deaths Analysis', 'Vaccinations Analysis'])

    if page == 'Cases Analysis':
        st.subheader('COVID-19 Cases Analysis')
        plot_cases_analysis(df)

    elif page == 'Deaths Analysis':
        st.subheader('COVID-19 Deaths Analysis')
        plot_deaths_analysis(df)
        plot_total_recovery_analysis(df)

    elif page == 'Vaccinations Analysis':
        st.subheader('COVID-19 Vaccinations Analysis')
        plot_vaccinations_analysis(df)

# Create a function to plot cases analysis
def plot_cases_analysis(df):
    plot_df_cases = df.groupby(['Unnamed: 0'])['imputed_total_cases'].sum().reset_index()
    fig = px.line(
        plot_df_cases,
        x='Unnamed: 0',
        y='imputed_total_cases',
        title='Total Cases Over Time',
        labels={'Unnamed: 0': '', 'imputed_total_cases': 'Total Cases'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Cases', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

# Create a function to plot deaths analysis
def plot_deaths_analysis(df):
    plot_df_deaths = df.groupby(['Unnamed: 0'])['imputed_total_deaths'].sum().reset_index()
    fig = px.line(
        plot_df_deaths,
        x='Unnamed: 0',
        y='imputed_total_deaths',
        title='Total Deaths Over Time',
        labels={'Unnamed: 0': '', 'imputed_total_deaths': 'Total Deaths'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Deaths', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

# Create a function to plot vaccinations analysis
def plot_vaccinations_analysis(df):
    plot_df_vaccinations = df.groupby(['Unnamed: 0'])['totalVaccinations'].sum().reset_index()
    fig = px.line(
        plot_df_vaccinations,
        x='Unnamed: 0',
        y='totalVaccinations',
        title='Total Vaccinations Over Time',
        labels={'Unnamed: 0': '', 'totalVaccinations': 'Total Vaccinations'},
        height=600
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=14))
    fig.update_yaxes(title_text='Total Vaccinations', title_font=dict(size=16))
    fig.update_layout(title_font=dict(size=24))
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()

# Create functions to display box plots
def cases_by_stringency_index(df):
    fig = px.box(df, x='stringency_index', y='imputed_total_cases',
                title='Cases by Stringency Index',
                width=800, height=800, color='stringency_index')
    st.plotly_chart(fig)

def totsl_deaths_by_stringency_index(df):
    fig = px.box(df, x='stringency_index', y='imputed_total_deaths',
                title='Total deaths by Stringency Index',
                width=800, height=800, color='stringency_index')
    st.plotly_chart(fig)     

def deaths_by_reproduction_rate(df):
    fig = px.box(df, x='reproduction_rate', y='imputed_total_deaths',
                title='Deaths by Reproduction Rate',
                width=800, height=800, color='reproduction_rate')
    st.plotly_chart(fig)

# Sidebar selector for user to choose a plot
plot_choice = st.sidebar.selectbox("Select a Plot", ["Cases by Stringency Index","Total Deaths Distribution by Stringency index", "Deaths by Reproduction Rate"])

# Instructions
st.sidebar.markdown("Explore the distribution of cases and deaths by selecting a plot.")

# Display the selected plot and title
if plot_choice == "Cases by Stringency Index":
    st.subheader("Cases Distribution by Stringency Index")
    cases_by_stringency_index(df)

elif plot_choice == "Deaths Distribution by Reproduction Rate":
    st.subheader("Deaths Distribution by Reproduction Rate")
    deaths_by_reproduction_rate(df)

else:
    st.subheader("Total Deaths Distribution by Stringency index")
    totsl_deaths_by_stringency_index(df) 
