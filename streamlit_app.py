## Smoothie Order Form ##
# streamlit docs: https://docs.streamlit.io/develop/api-reference/widgets/st.text_input

# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write(f'The name on your smoothie will be {name_on_order}')

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session() # session = cnx.session

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# my_dataframe = cnx.query("SELECT FRUIT_NAME FROM FRUIT_OPTIONS")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections = 5,
)

if ingredients_list:
    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',
            '""" + name_on_order + """')"""

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        # cnx.query(my_insert_stmt)
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
