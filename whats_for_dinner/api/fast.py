from datetime import datetime
import pytz
import pandas as pd
import io
import sys

from whats_for_dinner.ml_logic.registry import load_model
from whats_for_dinner.ml_logic.main import pred_streamlit
from whats_for_dinner.data.data import score_recipes

# from whats_for_dinner.ml_logic.preprocessor import preprocess_features

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# 💡 Preload the model to accelerate the predictions
app.state.model = load_model()


@app.get("/")
def index():
    return {"status": "OK"}


@app.post("/predict")
async def classification(img: UploadFile=File(...)):
    """
    receive image from user and return a predicted class
    """
    # initial type is <class 'starlette.datastructures.UploadFile'>



    # #contents = await img.read()

    # ### put images in a folder, "folder"
    # folder = ""
    # y_pred = pred(folder)
    # img = img.file.read()

    # predicted_class = pred_streamlit(img)

    # return predicted_class

    extension = img.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be .jpg, .jpeg or .png format!"

    # prediction = pred_streamlit(await img.read())

    # prediction = pred_docker(await img.read())
    print(f"img (straight from initial Upload) type: {type(img)}")

    img = img.file.read()
    # type after img.file.read() is <class 'bytes'>

    # img2 = img.read() ## results in TypeError: a bytes-like object is required, not 'coroutine' in main.py line 163
    # type after img.file.read() is <class 'coroutine'>

    # image = Image.open(io.BytesIO(image)).convert('RGB')

    predicted_class = pred_streamlit(img)
    app.state.predicted_class = predicted_class
    return predicted_class


@app.post("/recipe_pull")
async def recipes(recipes_num):
    """
    receive number of recipes desired by the user, and return
    """
    food_output = score_recipes(user_input=app.state.predicted_class,best_num=(int(recipes_num)))

    return food_output


@app.post("/predict2")
async def classification2(img: UploadFile=File(...)):
    """
    receive image from user and return a predicted class
    """
    img = img.file.read()

    # img = await img.read()

    predicted_class = pred_streamlit(img)
    app.state.predicted_class = predicted_class
    print(predicted_class)
    return predicted_class

@app.post("/recipe_pull2")
async def recipes2(recipes_num: int):
    """
    receive number of recipes desired by the user, and return
    """
    food_output = score_recipes(user_input=app.state.predicted_class,best_num=(int(recipes_num)))
    print(food_output)
    return food_output
