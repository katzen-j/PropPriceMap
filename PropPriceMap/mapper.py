from os.path import exists
import os
# from isort import file
import pandas as pd
import folium
from folium import IFrame
from folium.features import DivIcon
from branca.element import Figure
from requests import post
import matplotlib.pyplot as plt
from PropPriceMap.get_from_sql import get_user_input,town_city_connect, locality_connect, postcode_connect

def mapper(localities,towncities,user_input):
    ''' run through the mapping process
    includes checks if town or city exists '''

    city = get_user_input(user_input)
    
    if not isinstance(city, pd.DataFrame):
        return "none"

    #----------------------------------------------------------------------------
    mean_price = city.price.mean()
    median_price = city.price.median()
    # get the midpoints of latitude and longitude for future mapping
    mid_lat = ((max(city.latitude) - min(city.latitude))/2) + min(city.latitude)
    mid_lon = ((max(city.longitude) - min(city.longitude))/2) + min(city.longitude)

    # get price ranges
    price_min,price_max,price_range = min(city.price),max(city.price),max(city.price)-min(city.price)

    # return as dictionary
    city_dict = {"mid_lat": mid_lat,
                 "mid_long": mid_lon,
                 "price_min": price_min,
                 "price_max": price_max,
                 "price_range": price_range,
                 "city_df":city
                }

    #########################################################
    #### MAPPING
    #########################################################
    # fig, ax = plt.subplots()
    fig = Figure(width=800, height=600)

    map = folium.Map(location = [city_dict['mid_lat'], city_dict['mid_long']], zoom_start = 14)
    feature_group = folium.FeatureGroup("Locations")

    for lat, lng, price, poan, street, postcode, date in zip(city_dict['city_df'].latitude,
                                city_dict['city_df'].longitude,
                                city_dict['city_df'].price,
                                city_dict['city_df'].poan,
                                city_dict['city_df'].street,
                                city_dict['city_df'].postcode,
                                city_dict['city_df'].date):
        # feature_group.add_child(folium.Marker(location=[lat,lng],popup=name))
        t_tip = [f"£{price:,}", f"{poan} {street}, {postcode}",date.split()[0]]
        feature_group.add_child(folium.Circle(location=[lat,lng],
                                            tooltip=t_tip,
                                            radius=30*(price-price_min)/price_range,
                                            fill=True,
                                            color="red",
                                            fill_opacity=1.0*(1-(price-price_min)/price_range)))

    map.add_child(feature_group)

    fig.add_child(map)

    # mean_median_print = f"Average price: £{int(mean_price):,}  Median price: £{int(median_price):,}"
    # html_text = f'<div style="font-size: 10pt">{mean_median_print}</div>'
    # folium.map.Marker(
    #     [max(city.latitude)-0.005, mid_lon],
    #     icon=DivIcon(
    #         icon_size=(350,36),
    #         icon_anchor=(0,0),
    #         html=html_text,
    #         )
    #     ).add_to(map)

    return fig, [mean_price, median_price] #city_dict