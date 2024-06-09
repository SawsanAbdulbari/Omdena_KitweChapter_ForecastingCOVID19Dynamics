import streamlit as st
from st_pages.eda_page import main as eda_page
from st_pages.home_page import main as home_page
from st_pages.model_page import main as model_page
from st_pages.overview_page import main as overview_page
from st_pages.team_page import main as team_page

st.set_page_config(page_title='COVID-19 Case Prediction App', page_icon='assets/img/favicon.png', layout='wide')

home, overview, eda, model, team = st.tabs(['Home', 'Overview', 'EDA', 'Model', 'Team'])

home_page(home)
overview_page(overview)
eda_page(eda)
model_page(model)
team_page(team)