import streamlit as st
import pandas as pd
import requests
from PIL import Image


# Define two functions used to cleanup text, preferably should be done at the data preparation stage instead
def retrieve_instructions(cell):
    '''
    Cleans up the text in instructinos from the food df
    '''
    cell = cell.lstrip("c(")
    cell = cell.rstrip(")")
    cell = [line for line in [line.strip() for line in cell.split("\", \"")] if line]
    cell = [sentence.strip("\"") for sentence in cell]
    cell = '  \n  \n'.join(cell)
    return cell


def retrieve_ingredients(cell):
    '''
    Cleans up the text in ingredients from the food df
    '''
    cell = cell.lstrip("c(")
    cell = cell.rstrip(")")
    cell = [line for line in [line.strip() for line in cell.split("\", \"")] if line]
    cell = [word.strip("\"") for word in cell]
    cell = '  \n  \n'.join(cell)
    return cell


# Page header image and title
image1 = Image.open('../../raw_data/food.jpg')
st.image(image1, caption='copyright Ibrahim Hazm', width=400)

st.title("What's for Dinner? :spaghetti:", anchor="title")
subtitle = '<p style="font-family:sans-serif;color:red;font-weight:bold">Le Wagon - Data Science: Batch #991</p>'
st.markdown(subtitle, unsafe_allow_html=True)
st.write("#")

# Intro
st.header("Find recipe ideas.", anchor="1st step")
st.markdown(
    """
Short on **time**? ⏱

Not feeling **inspired**? 🧐

We've got the best and most delicious dishes to break you out of your weekday recipe rut.

"""
)
## API-run case

predict_uri = 'https://whatsfordinnernew-fua6zmtsfa-ew.a.run.app/predict2'
recipes_return_uri = 'https://whatsfordinnernew-fua6zmtsfa-ew.a.run.app/recipe_pull2'

st.write("#")


# Upload picture
st.header("Take a photo of an ingredient and upload it.", anchor="1st step")
img_file_buffer = st.file_uploader('')

classification_result = ""
st.write("#####")


# Preparing Streamlit session states
if "button1" not in st.session_state:
    st.session_state["button1"] = False

if "button2" not in st.session_state:
    st.session_state["button2"] = False

if "button3" not in st.session_state:
    st.session_state["button3"] = False


# Predict
if st.button('Get the ingredient!'):
    st.session_state["button1"] = not st.session_state["button1"]

# First streamlit state
if st.session_state["button1"]:
    st.image(Image.open(img_file_buffer), width=300) # "user_input" type is <class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>
    img_bytes = img_file_buffer.getvalue()
    response = requests.post(predict_uri, files={'img': img_bytes}, timeout=30)
    classification_result = response.json()
    pred = classification_result[0]

    st.header(f"It's {pred}!")
    st.write("#")

    st.header('Find a recipe.')


    # Ask for number of recipes
    best_num = int(st.number_input('How many recipes are you looking for?', min_value=1, max_value=8, step=1))

    if st.button('Show me the best recipes!'):
        st.session_state["button2"] = not st.session_state["button2"]


# Second streamlit state
if st.session_state["button1"] and st.session_state["button2"]:
    params = dict(recipes_num=best_num)
    response = requests.post(recipes_return_uri, params=params, timeout=30)
    output=response.json()
    food_df = pd.DataFrame.from_dict(output).reset_index()

    col1, col2 = st.columns(2)
    col1.subheader('Title')
    col2.subheader('Description')

    for index, row in food_df.iterrows():
        col1, col2 = st.columns(2)
        col1.write(f"{str(index + 1)}. {row['Name']}")
        col2.write(row['Description'])
    st.write("###")

    # Ask for final recipe choice
    recipe_choice = int(st.number_input('Which recipe would you like to make?', min_value=1, max_value=food_df.shape[0]+1, step=1))

    if st.button("Let's make it!"):
        st.session_state["button3"] = not st.session_state["button3"]


# Third streamlit state
# Show ingredients, instructions
if st.session_state["button3"]:
    st.markdown(
    """
    ### Ingredients
    """
    )
    st.write(retrieve_ingredients(food_df.iloc[recipe_choice - 1]['RecipeIngredientParts']))
    st.markdown(
    """
    ### Instructions
    """
    )
    st.write(retrieve_instructions(food_df.iloc[recipe_choice - 1]['RecipeInstructions']))


# Leave some whitespace
st.write("#")
st.write("#")
st.write("#")
st.write("#")
st.write("#")
st.write("#")
st.write("#")

# Footer
'''
This front-end queries the [what's for dinner API](https://dinner-fua6zmtsfa-ew.a.run.app/) built by batch #991 of the Le Wagon Data Science bootcamp.
'''
