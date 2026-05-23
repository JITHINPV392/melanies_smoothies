import streamlit as st
from snowflake.snowpark.functions import col

# 1. Title and App Setup
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# 2. Get the Name input
title = st.text_input('Name on Smoothie:')
st.write('The Name on the Smoothie will be:', title)

# 3. Establish the Connection FIRST
# This uses the secrets you put in Streamlit Cloud
cnx = st.connection("snowflake")
session = cnx.session()

# 4. Use the session to get data
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# 5. Multiselect for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = '' 
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    st.write(ingredients_string)

    # Define the statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + title + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
