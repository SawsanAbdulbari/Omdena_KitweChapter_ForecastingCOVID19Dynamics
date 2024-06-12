
import os
import streamlit as st
import streamlit_extras
from streamlit_extras.app_logo import add_logo
st.title("Welcome to the COVID-19 Case Prediction :green[App!] :health_worker::test_tube:\n\n")
# Insert the image at the top of the page
st.image("./media/img.jpg", use_column_width=True)

# Add a sidebar with a logo
# st.sidebar.image("logo.jpg", use_column_width='bool') 
# add_logo("omdena_zambia_highres.png", height=10)
# Sidebar for additional information
st.sidebar.title('COVID-19 Dashboard')
st.sidebar.image("./media/omdena_zambia_highres.png", use_column_width='always') 
st.sidebar.write("The COVID-19 Case Prediction📊📈")
st.sidebar.write("")
# <p>Developed with <span style='color:blue;'>❤</span> by <a href="" target="_blank"></a> </p>
# Signature
st.sidebar.write("")
st.sidebar.markdown(
    "Made with :green_heart: by "
    "[Omdena Kitwe, Zambia Chapter Team](https://www.linkedin.com/company/omdena-kitwe-zambia-chapter/) Visit [ Omdena](https://www.omdena.com/)")

st.markdown("""
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
""")
st.image("./media/omdena_logo.jpg", use_column_width=False)
# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
<div class="footer">
<p>Developed with <span style='color:blue;'>❤</span> by <a href="https://www.linkedin.com/company/omdena-kitwe-zambia-chapter/" target="_blank">Omdena Kitwe, Zambia Chapter Team</a> </p>
</div>
""", unsafe_allow_html=True)
