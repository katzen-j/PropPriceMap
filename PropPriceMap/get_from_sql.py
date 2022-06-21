import sqlite3
import pandas as pd
import os

# dataframe column headers
df_cols = ['ID', 'price', 'date', 'postcode', 'poan', 'street', 'locality',
       'town_city', 'county', 'latitude', 'longitude']

def get_user_input(user_input):
    """
    check the type of input i.e. town, city or postcode
    """
    user_input = user_input.upper()
    # create connection to SQL database
    conn = sqlite3.connect('SQL_data/gov_housing_data_lite')
    c = conn.cursor()  

    # first check for town/city:
    query = """
    SELECT *
    FROM gov_data_db as gd
    WHERE gd.town_city = ?
    """
    c.execute(query, (user_input,))
    # returns a list
    datarows = c.fetchall()
    
    # check if data present and return constructed dataframe if true
    if len(datarows) > 0:
        datarows = pd.DataFrame(datarows, columns=df_cols)
        return datarows
    
    # if no towns or cities present, check if input is a locality
    else:
        query = """
        SELECT *
        FROM gov_data_db as gd
        WHERE gd.locality = ?
        """
        c.execute(query, (user_input,))
        # returns a list
        datarows = c.fetchall()
        
        # check if it's a locality and return constructed dataframe if true
        if len(datarows) > 0:
            datarows = pd.DataFrame(datarows, columns=df_cols)
            return datarows
        
        # if not a towncity or locailty, might be a postcode
        query = """
        SELECT *
        FROM gov_data_db as gd
        WHERE gd.postcode LIKE ?
        """
        c.execute(query, (user_input+"%",))
        # returns a list
        datarows = c.fetchall()
        
        # check if its a postcode and return constructed dataframe if true
        if len(datarows) > 0:
            datarows = pd.DataFrame(datarows, columns=df_cols)
            return datarows    
        # user input not found in database
        else:
            return "none"
        
