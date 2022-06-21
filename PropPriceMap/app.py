import streamlit as st
from mapper import mapper
import pandas as pd
import os
from streamlit_folium import folium_static, st_folium
import folium

# reduce padding at top of page
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# title
st.markdown('''
# Mapper
''')

# further info
st.markdown('''### 2021 Property Prices from UK Land Registry Data''')

# for checking paths, default not used
# st.write(os. getcwd())

# use session state to ensure displayed maps persist
if "map_show" not in st.session_state:
    st.session_state.map_show = False

# text box
user_input = st.text_input(label='Please enter a town/city or full postcode (with spaces) or first outward code (e.g. WD6) and press ENTER to display:', max_chars=40)

if user_input or st.session_state.map_show:
    output = mapper(user_input)
    if output == "none":
        st.write(f"{user_input} not found in database, please try again")
    else:
        output_map = output[0]
        st_data = st_folium(output_map, width = 725, height = 500)
        
        # further information
        region_info = f"The average house price is **£{output[1][0]:,.0f}** and the median is **£{output[1][1]:,.0f}**."
        st.markdown(region_info)
