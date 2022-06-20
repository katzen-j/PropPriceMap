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
from PropPriceMap.get_from_sql import town_city_connect, locality_connect, postcode_connect

def mapper(localities,towncities):
    ''' run through the mapping process
    includes checks if town or city exists '''

    # Determine postcode or towncity search
    post_city = input("Search by town/city [0] or postcode [1]")
    post_city = int(post_city)

        #############################################################################
        #  POSTCODE CHECKING
        #############################################################################
    if post_city == 1:
        postcode_user = input("Please enter full postcode (with spaces) or first outward code (e.g. WD6):")
        postcode_user = postcode_user.upper()
        
        # get postcode data from SQL
        city = postcode_connect(postcode_user)
        
        # check if any value inside dataframe else return not found
        if len(city) == 0:
            return "Postcode not found, please try again"

    else:
        #############################################################################
        #  TOWN CITY CHECKING
        #############################################################################
        # input town or city name then convert it to all uppper case
        name = input("Enter town or city name > ")
        name = name.upper()

        # check if this is a valid name and keep in loop until
        # valid name has been entered
        file_list_locales = localities
        file_list_towncities = towncities
        # flag to determine if localities or towncities columns should be searched
        # 1 for locales / 2 for towncities
        tc_flag = 0

        if name in file_list_locales:
            print(f"{name} found")
            tc_flag = 1
        elif name in file_list_towncities:
            print(f"{name} found")
            tc_flag = 2
        else:
            print(f"{name} not found")
            # stay in while loop until a valid name is provided
            name_count = 0 # give user 3 tries
            while not name in file_list_locales or not name in file_list_towncities and name_count < 2:
                name = input("Please enter a valid town or city name > ")
                name = name.upper()
                name_count += 1
                # exit if user has not typed in valid name 3 times
                if name_count >= 2:
                    return print("Could not find this town, please try again")
            if name in file_list_locales:
                tc_flag = 1
            elif name in file_list_towncities:
                tc_flag = 2
            print(f"{name} found! Proceeding..")

        # read in the selected city as a dataframe
        if tc_flag == 1: # search localities
            # city = gov_data_df[gov_data_df.locality == name]
            city = locality_connect(name)
            
            
        elif tc_flag == 2: # search towncities
            # city = gov_data_df[gov_data_df.town_city == name]
            city = town_city_connect(name)

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

    mean_median_print = f"Average price: £{int(mean_price):,}  Median price: £{int(median_price):,}"
    html_text = f'<div style="font-size: 10pt">{mean_median_print}</div>'
    folium.map.Marker(
        [max(city.latitude)-0.005, mid_lon],
        icon=DivIcon(
            icon_size=(350,36),
            icon_anchor=(0,0),
            html=html_text,
            )
        ).add_to(map)

    return fig #city_dict