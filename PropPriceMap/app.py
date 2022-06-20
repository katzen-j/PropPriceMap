import streamlit as st
from PropPriceMap.mapper import mapper
import pandas as pd
import os
from streamlit_folium import folium_static, st_folium
import folium

st.markdown('''
# Mapper
''')
st.markdown('''### 2021 Property Prices from UK Land Registry Data''')
# st.write(os. getcwd())
if "map_show" not in st.session_state:
    st.session_state.map_show = False

user_input = st.text_input(label='Please enter a town/city or full postcode (with spaces) or first outward code (e.g. WD6) and press ENTER to display:', max_chars=40)
# if st.button("Get results") or st.session_state.map_show:
if user_input or st.session_state.map_show:
    # st.session_state.map_show = False
    output = mapper(user_input)
    if output == "none":
        st.write(f"{user_input} not found in database, please try again")
    # elif st.session_state.map_show == True:
    else:
        output_map = output[0]
        st_data = st_folium(output_map, width = 725, height = 500)
        # st.st_folium(output, width = 725)
        
        region_info = f"The average house price is **£{output[1][0]:,.0f}** and the median is **£{output[1][1]:,.0f}**."
        st.markdown(region_info)
