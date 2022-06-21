import pandas as pd
import folium
from folium.features import DivIcon
from branca.element import Figure
from get_from_sql import get_user_input

def mapper(user_input):
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

        t_tip = [f"£{price:,}", f"{poan} {street}, {postcode}",date.split()[0]]
        feature_group.add_child(folium.Circle(location=[lat,lng],
                                            tooltip=t_tip,
                                            radius=30*(price-price_min)/price_range,
                                            fill=True,
                                            color="red",
                                            fill_opacity=1.0*(1-(price-price_min)/price_range)))

    map.add_child(feature_group)

    fig.add_child(map)

    return fig, [mean_price, median_price]