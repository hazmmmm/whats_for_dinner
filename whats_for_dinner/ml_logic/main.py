from tokenize import String
from whats_for_dinner.ml_logic.img_data_input_01 import create_images_df
from whats_for_dinner.ml_logic.preprocessor_01 import create_processed_images_df, create_processed_images_df_eval
from whats_for_dinner.ml_logic.params_01 import LOCAL_DATA_PATH
from whats_for_dinner.ml_logic.model_basic_01 import initialize_model, compile_model, train_model, evaluate_model
from whats_for_dinner.ml_logic.registry import load_model, save_model, get_model_version

from colorama import Fore, Style

import os
import numpy as np
import pandas as pd

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

    # start the model

    model = initialize_model()

    # model params
    learning_rate = 0.001
    patience = 5
    batch_size = 32

    model = compile_model(model, learning_rate)
    model, history = train_model(model, train_images, val_images, patience, batch_size)
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
    new_data_path = ""
    #new_data =

    if new_data_path is None:
        print("\n✅ no data to evaluate")
        return None

    eval_df = create_images_df(new_data_path)
    eval_images = create_processed_images_df_eval(eval_df)

    model = load_model()

    metrics_dict = evaluate_model(model, eval_images)
    metrics_accuracy = metrics_dict["val_accuracy"]

    # save evaluation
    params = dict(
        model_version=get_model_version(),
        # package behavior
        context="evaluate",
        )

    save_model(params=params, metrics=dict(val_accuracy=metrics_accuracy))

    return metrics_accuracy


def pred(X_pred):
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ use case: predict")

    # from taxifare.ml_logic.registry import load_model

    if X_pred is None:

        pass

    model = load_model()

    X_processed = preprocess_features(X_pred)

    y_pred = model.predict(X_processed)

    print("\n✅ prediction done: ", y_pred, y_pred.shape)

    return y_pred
