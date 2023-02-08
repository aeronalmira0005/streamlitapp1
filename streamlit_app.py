
import streamlit
import pandas as pd
import requests
from urllib.error import URLError

import snowflake.connector

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_list = fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect('Pick some fruits:', list(fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")

  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
   streamlit.error()  

streamlit.header("The fruit load list contains:")

if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input("What fruit would you like to add?", "jackfruit")
streamlit.write('Thanks for adding ', add_my_fruit)
