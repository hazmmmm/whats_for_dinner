from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from whats_for_dinner.ml_logic.registry_docker import load_model
from whats_for_dinner.ml_logic.main import pred_streamlit
from whats_for_dinner.data.data import score_recipes

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
    # ### put images in a folder, "folder"
    # folder = ""
    # y_pred = pred(folder)
    # img = img.file.read()

    # predicted_class = pred_streamlit(img)

    # return predicted_class

    extension = img.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be .jpg, .jpeg or .png format!"

    img = img.file.read()
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
    return food_output
