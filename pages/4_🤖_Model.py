import streamlit as st
from predictions_page.model_total_death_prediction import total_death_prediction_page
from predictions_page.model_total_case_prediction import total_case_prediction_page

def main():
    # Sidebar for additional information
    st.sidebar.title('COVID-19 Dashboard')
    st.sidebar.image("./media/omdena_zambia_highres.png", use_column_width='always') 
    st.sidebar.write("This dashboard provides two prediction model options to predict total death and total cases.")
    st.sidebar.divider()


    st.sidebar.title("Prediction Menu")
    options = st.sidebar.radio("Select a Prediction Model:", ["Total Death Prediction", "Total Case Prediction"])

    if options == "Total Death Prediction":
        total_death_prediction_page()
    elif options == "Total Case Prediction":
        total_case_prediction_page()

if __name__ == "__main__":
    main()
