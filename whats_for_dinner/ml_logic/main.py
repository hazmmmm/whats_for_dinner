from tokenize import String
from keras.applications.vgg16 import preprocess_input
# from keras.utils.image_utils import img_to_array, load_img
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from whats_for_dinner.ml_logic.preprocessor import create_processed_images_df, create_processed_images_df_eval, create_images_df, create_pred_images_df, create_processed_images_df_pred, proc_img
from whats_for_dinner.ml_logic.params import LOCAL_DATA_PATH
# from whats_for_dinner.ml_logic.model_basic import initialize_model, compile_model, train_model, evaluate_model
from whats_for_dinner.ml_logic.model_vgg16 import initialize_model, compile_model, train_model, evaluate_model
from whats_for_dinner.ml_logic.registry import load_model, save_model, get_model_version, save_labels, load_labels
from whats_for_dinner.data.data import score_recipes

from colorama import Fore, Style

import os
import numpy as np
import pandas as pd

from io import BytesIO
from PIL import Image

def preprocess_and_train():
    '''
    Preprocess the image data.
    Parameters:
    '''
    # TO-DO!!
    # Create two paths, using IFs. 1 for local storage and 1 for when it's in a bucket
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

    # start the model

    model = initialize_model(train_df)

    # model params
    learning_rate = 0.0001
    patience = 6
    batch_size = 32
    epochs = 100
    # epochs = 1

    model = compile_model(model, learning_rate)
    model, history = train_model(model, train_images, val_images, patience, batch_size, epochs)
    metrics_accuracy = np.max(history.history['val_accuracy'])
    print(f"\n✅ trained with accuracy: {round(metrics_accuracy, 2)}")

    params = dict(
        # model parameters
        learning_rate=learning_rate,
        batch_size=batch_size,
        patience=patience,
        # package behavior
        context="train",
        # data source
        model_version=get_model_version(),
    )

    # save model
    save_model(model=model, params=params, metrics=dict(val_accuracy=metrics_accuracy))

    return metrics_accuracy

def evaluate():
    """
    Evaluate the performance of the latest production model on new data
    """

    print("\n⭐️ use case: evaluate")

    # load new data
    new_data_path = os.path.join(LOCAL_DATA_PATH, "eval")

    if new_data_path is None:
        print("\n✅ no data to evaluate")
        return None

    eval_df = create_images_df(new_data_path)
    eval_images = create_processed_images_df_eval(eval_df)

    model = load_model()

    metrics = evaluate_model(model, eval_images)
    metrics_accuracy = metrics[1]

    # save evaluation
    params = dict(
        model_version=get_model_version(),
        # package behavior
        context="evaluate",
        )

    save_model(params=params, metrics=dict(val_accuracy=metrics_accuracy))

    return metrics_accuracy


def pred(user_input = None):
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ use case: predict")

    # from taxifare.ml_logic.registry import load_model


    # folder path
    if user_input is None:

        user_input = '../../raw_data/fruits_and_vegetables_image_recognition_dataset/pred'

    pred_df = create_pred_images_df(user_input)
    pred_images = create_processed_images_df_pred(pred_df)


    # # single-image path

    # img = Image.open(user_input)
    # pred_images = img.resize((224, 224))



    labels = load_labels()
    labels = dict(enumerate(labels.flatten()))
    labels = labels[0]
    print("Changed labels into dict")
    print(type(labels))

    model = load_model()

    predicted_probabilities = model.predict(pred_images)



    if len(predicted_probabilities) == 1:
        print("Prediction done on one input.")
        predicted_probabilities = np.argmax(predicted_probabilities,axis=1)[0]
        y_pred = labels[predicted_probabilities]
        print("\n✅ prediction done: ", y_pred)
    else:
        print(f"Prediction done on {len(predicted_probabilities)} inputs.")
        predicted_probabilities = np.argmax(predicted_probabilities,axis=1)
        y_pred = [labels[k] for k in predicted_probabilities]

        print("\n✅ prediction done: ", y_pred)

    return y_pred

def pred_streamlit(user_input):

    image = Image.open(BytesIO(user_input))
    print(f"type after Image.open: {type(image)}")

    # #
    # image = load_img(image, target_size=(224, 224))
    # image = load_img(user_input, target_size=(224, 224))
    image = image.resize((224,224))
    print(f"type after resize: {type(image)}")


    # convert the image pixels to a numpy array
    image = img_to_array(image)
    print(f"type after img_to_array: {type(image)}")


    # reshape data for the model
    image = image.reshape((1,224,224,3))
    print(f"type after reshape: {type(image)}")



    # prepare the image for the VGG model
    image = preprocess_input(image)
    print(f"type after preprocess_input: {type(image)}")


    #predict me!
    model = load_model()
    result = model.predict(image)
    predicted_probabilities = np.argmax(result,axis=1)
    labels = load_labels()
    labels = dict(enumerate(labels.flatten()))
    labels = labels[0]

    pred = [labels[k] for k in predicted_probabilities]

    return pred


def recipe_pull():
    food_output = print(score_recipes(user_input=pred(),best_num=(int(input("How many recipes do you want? ")))))
    return food_output


def test_docker_print():
    print("Hello hello!")
    return


if __name__ == '__main__':
    # preprocess_and_train()
    # evaluate()
    pred()
    # recipe_pull()
    test_docker_print()
