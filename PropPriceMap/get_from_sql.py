import sqlite3
import pandas as pd
import os

# dataframe column headers
df_cols = ['ID', 'price', 'date', 'postcode', 'poan', 'street', 'locality',
       'town_city', 'district', 'county', 'latitude', 'longitude']

def town_city_connect(towncity):
    """
    Input a town or city and return a dataframe of
    house prices in that area
    """
    # create connection to SQL database
    conn = sqlite3.connect('raw_data/gov_housing_data_SQL')
    c = conn.cursor()
    
    query = """
    SELECT *
    FROM gov_data_db as gd
    WHERE gd.town_city = ?
    """
    c.execute(query, (towncity,))
    datarows = c.fetchall()
    datarows = pd.DataFrame(datarows, columns=df_cols)
    
    c.close()
    conn.close()
    
    return datarows

def locality_connect(locality):
    """
    Input a locality and return a dataframe of
    house prices in that area
    """
    # create connection to SQL database
    conn = sqlite3.connect('raw_data/gov_housing_data_SQL')
    c = conn.cursor()
    
    query = """
    SELECT *
    FROM gov_data_db as gd
    WHERE gd.locality = ?
    """
    c.execute(query, (locality,))
    datarows = c.fetchall()
    datarows = pd.DataFrame(datarows, columns=df_cols)
    
    c.close()
    conn.close()
    
    return datarows

def postcode_connect(postcode_user):
    """
    Input a postcode, partial or full and return a dataframe of
    house prices in that postcode
    """
    # create connection to SQL database
    conn = sqlite3.connect('raw_data/gov_housing_data_SQL')
    c = conn.cursor()
    
    query = """
    SELECT *
    FROM gov_data_db as gd
    WHERE gd.postcode LIKE ?
    """
    c.execute(query, (postcode_user+"%",))
    datarows = c.fetchall()
    datarows = pd.DataFrame(datarows, columns=df_cols)
    
    c.close()
    conn.close()
    
    return datarows