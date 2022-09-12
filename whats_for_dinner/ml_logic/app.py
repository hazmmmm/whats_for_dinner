import streamlit as st
import numpy as np
import pandas as pd
import os
import requests
from whats_for_dinner.data.data import score_recipes
from whats_for_dinner.ml_logic.main import pred_streamlit


from PIL import Image

image1 = Image.open('../../raw_data/food.jpg')
st.image(image1, caption='copyright Ibrahim Hazm', width=400)


st.title("What's for dinner :spaghetti:", anchor="title")
subtitle = '<p style="font-family:sans-serif;color:red;font-weight:bold">Le Wagon - Data Science</p>'
st.markdown(subtitle,unsafe_allow_html=True)


#'''


#TO UPDATE !! This front queries the Le Wagon [taxi fare model API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
#'''
#RESUME
st.markdown('''
Well, here we go again, grocery time ...:sleepy:

Hey you know what? I'm tired of always eating the same thing, let's change!
I want to try out this ingredient but don't know what to do with it :thinking_face:
''')

#UPLOAD PICTURE
st.header("Upload a picture", anchor="1st step")
user_input = st.file_uploader('')

#PREDICTION
if st.button('predict'):
    # print is visible in the server output, not in the page
    st.image(user_input)
    # pred = st.write(pred_streamlit(user_input))
    pred = st.write(pred_streamlit(user_input.read()))


else:
    st.write('click me :point_up_2:')


#NUMBER OF RECIPES
best_num = int(st.number_input('How many recipes do you want?', min_value=1, max_value=8, step=1, value=5))
if st.button('Show me the best recipes'):
    # print is visible in the server output, not in the page
    food_output = st.write(score_recipes(pred_streamlit(user_input.read()),best_num))

else:
    st.write('click me :spaghetti:')



#csv_path2 = os.path.join('raw_data')
#recipes_cleaned = pd.read_csv('/home/clara/code/hazmmmm/whats_for_dinner/raw_data/recipes_cleaned.csv')
#'''display the original dataframe'''
#st.dataframe(recipes_cleaned.head(4))
