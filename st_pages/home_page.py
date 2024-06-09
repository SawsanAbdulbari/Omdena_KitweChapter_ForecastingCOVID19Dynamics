import streamlit as st
from streamlit_lottie import st_lottie

def main(home):
    cols = home.columns(2)

    with cols[0]:
        st.write("<br>"*5, unsafe_allow_html=True)
        st.image("assets/img/banner.png", use_column_width=True)
        st.write("""
            <center>
                <h1>Welcome to the COVID-19 Case Prediction App! 🧑‍⚕️🧪</h1> 
            </center>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        st.write("<br>"*3, unsafe_allow_html=True)
        st_lottie("https://lottie.host/00c554d8-f352-4ed4-85c7-5c4e2610c092/TGx4z8xXUg.json")

    home.markdown(f"""
    {'<br>'*9}
    ## Project Background
    In Zambia, like many countries worldwide, the COVID-19 pandemic has posed significant challenges to public health, socioeconomic stability, and everyday life. With the virus continuing to spread and evolve, accurate forecasting of COVID-19 dynamics is essential for guiding decision-making, resource allocation, and public health interventions.

    ### Challenge Background
    As the pandemic unfolded, Zambia, like other nations, faced a multitude of challenges in managing the spread of the virus. These challenges included limited healthcare resources, logistical constraints, socioeconomic disparities, and the complexities of implementing public health measures in diverse and often remote regions.

    ### Project Goals
    - :dart: **Develop a predictive model** to forecast COVID-19 spread in Kitwe, Zambia.
    - :bar_chart: **Analyze historical COVID-19 data** specific to Kitwe to identify patterns, trends, and potential drivers of virus transmission.
    - :clipboard: **Provide actionable insights and forecasts** to local decision-makers, healthcare professionals, and community leaders.
    - :mega: **Enhance public awareness and engagement** regarding COVID-19 by disseminating accurate and localized information.
    - :handshake: **Foster collaboration and partnerships** between local stakeholders to collectively address the challenges posed by the pandemic.

    ### How to Use This App
    1. :point_right: Navigate to the [**Model**](#model) page.
    2. :writing_hand: Enter the required input features.
    3. :chart_with_upwards_trend: Get the predicted total imputed cases.

    **Note:** Ensure that all input fields are filled in accurately for the best prediction results.

    ### Useful Links
    - [World Health Organization (WHO)](https://www.who.int/) :earth_africa:
    - [Zambia Ministry of Health](https://www.moh.gov.zm/) :flag-zm:
    - [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) :bar_chart:
    - [Our World in Data: COVID-19 Data](https://ourworldindata.org/coronavirus) :globe_with_meridians:

    ### Contact Us
    For more information, please reach out to our team at [info@covidpredictapp.com](mailto:info@covidpredictapp.com) :email:
    """, unsafe_allow_html=True)