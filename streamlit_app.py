## Smoothie Order Form ##
# streamlit docs: https://docs.streamlit.io/develop/api-reference/widgets/st.text_input

# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

# option = st.selectbox("What is your favorite fruit?",("Banana","Strawberries","Peaches"))
# st.write("Your favorite fruit is:", option)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections = 5,
)

name_on_order = st.text_input("Name on Smoothie:")
st.write(f'The name on your smoothie will be {name_on_order}')

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
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
