import streamlit as st
from streamlit import session_state
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
st.markdown(subtitle, unsafe_allow_html=True)


#'''

#TO UPDATE !! This front queries the Le Wagon [taxi fare model API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
#'''

# RESUME
st.header("Find recipe ideas.", anchor="1st step")
st.markdown(
    """
Feeling short on time and short on dinner inspiration? We’ve got the best and delicious dishes to break you out of your weekday recipe rut.

Search by the ingredients themselves by uploading a picture, then add filters like the type of meal and add any dietary restrictions.
"""
)

# UPLOAD PICTURE

user_input = st.file_uploader("Upload a picture")


if 'key' not in session_state:
    session_state.key = 0

#UPLOAD PICTURE
st.header("Upload a picture", anchor="1st step")
user_input = st.file_uploader('')

#PREDICTION
if st.button('predict'):
    # print is visible in the server output, not in the page
    st.image(user_input) # "user_input" type is <class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>
    # print(f"user_input.read() type: {type(user_input.read())}") ## breaks the code.

    # pred = st.write(pred_streamlit(user_input))
    pred = st.write(pred_streamlit(user_input.read())) ## "pred" type is <class 'NoneType'> ?????
    # pred = st.write(pred_streamlit(user_input.file.read()))



#NUMBER OF RECIPES
best_num = int(st.number_input('How many recipes do you want?', min_value=1, max_value=8, step=1, value=5))
if st.button('Show me the best recipes'):
    # print is visible in the server output, not in the page
    food_output = st.write(score_recipes(pred_streamlit(user_input.read()),best_num))

else:
    st.write('click me :spaghetti:')

# NUMBER OF RECIPES
if st.button("Show me the best recipes"):

     food_output = st.write(score_recipes(pred_streamlit(user_input), best_num))

else:
    st.write("click me :spaghetti:")
