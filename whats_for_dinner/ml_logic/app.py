from warnings import filters
import streamlit as st
from streamlit import session_state
import numpy as np
import pandas as pd
import os
import requests
from PIL import Image

# from whats_for_dinner.data.data import score_recipes
# from whats_for_dinner.ml_logic.main import pred_streamlit


image1 = Image.open("../../raw_data/food.jpg")
st.image(image1, caption="copyright Ibrahim Hazm", width=400)


st.title("What's for dinner :spaghetti:", anchor="title")
subtitle = '<p style="font-family:sans-serif;color:red;font-weight:bold">Le Wagon - Data Science</p>'
st.markdown(subtitle, unsafe_allow_html=True)


"""
 This front queries batch  #991 [what's for dinner model API](https://whatsfordinner-fua6zmtsfa-ew.a.run.app)
"""

# RESUME
st.header("Find recipe ideas.", anchor="1st step")
st.markdown(
    """
Feeling short on time and short on dinner inspiration? We’ve got the best and delicious dishes to break you out of your weekday recipe rut.

Search by the ingredients themselves by uploading a picture, then add filters like the type of meal and add any dietary restrictions.
"""
)

## API-run case
predict_uri = "https://whatsfordinner-fua6zmtsfa-ew.a.run.app/predict2"
recipes_return_uri = ("https://whatsfordinner-fua6zmtsfa-ew.a.run.app/recipe_pull2?recipes_num=5")

# UPLOAD PICTURE
st.header("Upload a picture", anchor="1st step")
img_file_buffer = st.file_uploader("")

classification_result = ""

# PREDICTION
load = st.button("Get the ingredient!")

# Initialize session state
if "load_state" not in st.session_state:
    st.session_state.load_state = False

if load or st.session_state.load_state:
    st.session_state.load_state = True

    # print is visible in the server output, not in the page
    st.image(
        Image.open(img_file_buffer), width=300
    )  # "user_input" type is <class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>
    img_bytes = img_file_buffer.getvalue()
    response = requests.post(predict_uri, files={"img": img_bytes})
    classification_result = response.json()
    pred = classification_result[0]

    st.caption(f"your ingredient is: {pred}")

# NUMBER OF RECIPES
best_num = int(
    st.number_input(
        "How many recipes do you want?", min_value=1, max_value=8, step=1, value=5
    )
)

if st.button("Show me the best recipes!"):
    params = dict(recipes_num=best_num)
    response = requests.post(recipes_return_uri, params=params)
    output = response.json()
    food_output = output["Name"]
    for value in food_output.values():
        st.write(value)

    # testing to display review count
    revcount = output["ReviewCount"]
    st.write(revcount["250"])
    # variable avec filters
    # checkboxs -total time etc...)
