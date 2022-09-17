import os
from io import BytesIO
import numpy as np

from colorama import Fore, Style
from PIL import Image

from keras.applications.vgg16 import preprocess_input

# Tensorflow imports for M1 MB
from tensorflow.keras.preprocessing.image import img_to_array

# Tensorflow imports for other
# from keras.utils.image_utils import img_to_array, load_img

# whats_for_dinner local imports
from whats_for_dinner.ml_logic.preprocessor import create_processed_images_df, create_processed_images_df_eval, \
create_images_df, create_pred_images_df, create_processed_images_df_pred, proc_img
from whats_for_dinner.ml_logic.params import LOCAL_DATA_PATH, LEARNING_RATE, BATCH_SIZE, EPOCHS, PATIENCE
from whats_for_dinner.ml_logic.registry_docker import load_model, save_model, get_model_version, save_labels, load_labels
from whats_for_dinner.data.data import score_recipes

# Choice of model - basic conv2 model or vgg16 model
# from whats_for_dinner.ml_logic.model_basic import initialize_model, \
    # compile_model, train_model, evaluate_model
from whats_for_dinner.ml_logic.model_vgg16 import initialize_model, compile_model, \
    train_model, evaluate_model




def preprocess_and_train():
    '''
    Preprocess the image data.
    Parameters:
    '''

    # Get paths
    train_path = os.path.join(LOCAL_DATA_PATH, "train")
    val_path = os.path.join(LOCAL_DATA_PATH, "validation")
    test_path = os.path.join(LOCAL_DATA_PATH, "test")
    # Get the dfs with filepaths for all the images
    train_df = create_images_df(train_path)
    val_df = create_images_df(val_path)
    test_df = create_images_df(test_path)

    # Create DataFrameIterator's for train, val and test
    train_images, val_images, test_images = create_processed_images_df(train_df, val_df, test_df)
    labels = (train_images.class_indices)
    labels = dict((v,k) for k,v in labels.items())
    save_labels(labels)

    # Start the model
    model = initialize_model(train_df)

    # Compile the model
    model = compile_model(model, LEARNING_RATE)

    # Train the model
    model, history = train_model(model, train_images, val_images, PATIENCE, BATCH_SIZE, EPOCHS)
    metrics_accuracy = np.max(history.history['val_accuracy'])
    print(f"\n✅ trained with accuracy: {round(metrics_accuracy, 2)}")

    # Save parameters
    params = dict(
        # Model parameters
        learning_rate=LEARNING_RATE,
        batch_size=BATCH_SIZE,
        patience=PATIENCE,
        # Package behavior
        context="train",
        # Data source
        model_version=get_model_version(),
    )

    # Save model
    save_model(model=model, params=params, metrics=dict(val_accuracy=metrics_accuracy))

    return metrics_accuracy

def evaluate():
    """
    Evaluate the performance of the latest production model on new data
    """

    print("\n⭐️ use case: evaluate")

    # Load new data
    new_data_path = os.path.join(LOCAL_DATA_PATH, "eval")

    if new_data_path is None:
        print("\n✅ no data to evaluate")
        return None

    # Get df and create DataFrameIterator
    eval_df = create_images_df(new_data_path)
    eval_images = create_processed_images_df_eval(eval_df)

    # Load saved model
    model = load_model()

    # Evaluate
    metrics = evaluate_model(model, eval_images)
    metrics_accuracy = metrics[1]

    # Save evaluation
    params = dict(
        model_version=get_model_version(),
        # package behavior
        context="evaluate",
        )

    # Save model
    save_model(params=params, metrics=dict(val_accuracy=metrics_accuracy))

    return metrics_accuracy


def pred(user_input = None):
    """
    Make a prediction using the latest trained model, using folders as input
    """
    print("\n⭐️ use case: predict")

    ## Folder path
    if user_input is None:

        user_input = '../../raw_data/fruits_and_vegetables_image_recognition_dataset/pred'

    # Get df and create DataFrameIterator
    pred_df = create_pred_images_df(user_input)
    pred_images = create_processed_images_df_pred(pred_df)

    # Load labels from trained model to match names to the output classes
    labels = load_labels()
    labels = dict(enumerate(labels.flatten()))
    labels = labels[0]

    # Load model
    model = load_model()

    # Get predictions
    predicted_probabilities = model.predict(pred_images)

    if len(predicted_probabilities) == 1:
        print(Fore.BLUE + "\nPrediction done on one input." + Style.RESET_ALL)
        predicted_probabilities = np.argmax(predicted_probabilities,axis=1)[0]
        y_pred = labels[predicted_probabilities]
        print("\n✅ prediction done: ", y_pred)
    else:
        print(Fore.BLUE + f"Prediction done on {len(predicted_probabilities)} inputs." + Style.RESET_ALL)
        predicted_probabilities = np.argmax(predicted_probabilities,axis=1)
        y_pred = [labels[k] for k in predicted_probabilities]

        print("\n✅ prediction done: ", y_pred)

    return y_pred


def pred_streamlit(user_input):
    """
    Make a prediction using the latest trained model, using a single image as input
    """
    image = Image.open(BytesIO(user_input))
    print(f"type after Image.open: {type(image)}")

    # Resize to 224 x 224
    image = image.resize((224,224))
    print(f"type after resize: {type(image)}")

    # Convert the image pixels to a numpy array
    image = img_to_array(image)
    print(f"type after img_to_array: {type(image)}")

    # Reshape data for the model
    image = image.reshape((1,224,224,3))
    print(f"type after reshape: {type(image)}")

    # Prepare the image for the VGG model
    image = preprocess_input(image)
    print(f"type after preprocess_input: {type(image)}")

    # Run prediction
    model = load_model()
    result = model.predict(image)
    predicted_probabilities = np.argmax(result,axis=1)
    labels = load_labels()
    labels = dict(enumerate(labels.flatten()))
    labels = labels[0]

    prediction = [labels[k] for k in predicted_probabilities]

    return prediction


def recipe_pull():
    '''
    Get recipes
    '''
    food_output = print(score_recipes(user_input=pred(),best_num=(int(input("How many recipes do you want? ")))))
    return food_output


def test_docker_print():
    '''
    Just a tester function
    '''
    print("Hello hello!")
    return


if __name__ == '__main__':
    # preprocess_and_train()
    # evaluate()
    # pred()
    # recipe_pull()
    test_docker_print()
