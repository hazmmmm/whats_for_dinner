from datetime import datetime
import pytz
import pandas as pd
import io
import sys

from whats_for_dinner.ml_logic.registry import load_model
from whats_for_dinner.ml_logic.main import pred_streamlit

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
async def receive_image(img: UploadFile=File(...)):
    """
    receive image from user
    """
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

    # try:
    # img = img.file.read()
    img = img.read()
    # image = Image.open(io.BytesIO(image)).convert('RGB')

    predicted_class = pred_streamlit(img)

    return predicted_class

    # except Exception as error:
    #     # e = sys.exc_info()[1]
    #     # raise HTTPException(status_code=500, detail=str(e))
    #     pass

    # return prediction
