'''
Module for saving and loading models, params and class labels for a Docker run
'''

import glob
import os
import time
import pickle
import numpy as np

from colorama import Fore, Style

from tensorflow.keras import Model, models

from whats_for_dinner.ml_logic.params import LOCAL_REGISTRY_PATH, RUN_TYPE


def save_model(model: Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    Persist trained model, params and metrics
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # if os.environ.get("MODEL_TARGET") == "mlflow":

    #     # retrieve mlflow env params
    #     mlflow_tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    #     mlflow_experiment = os.environ.get("MLFLOW_EXPERIMENT")
    #     mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

    #     # configure mlflow
    #     mlflow.set_tracking_uri(mlflow_tracking_uri)
    #     mlflow.set_experiment(experiment_name=mlflow_experiment)

    #     with mlflow.start_run():

    #         # STEP 1: push parameters to mlflow
    #         if params is not None:
    #             mlflow.log_params(params)

    #         # STEP 2: push metrics to mlflow
    #         if metrics is not None:
    #             mlflow.log_metrics(metrics)

    #         # STEP 3: push model to mlflow
    #         if model is not None:

    #             mlflow.keras.log_model(keras_model=model,
    #                                    artifact_path="model",
    #                                    keras_module="tensorflow.keras",
    #                                    registered_model_name=mlflow_model_name)

    #     print("\n✅ data saved to mlflow")

    #     return None

    print(Fore.BLUE + "\nSave model to local disk..." + Style.RESET_ALL)

    # Save params
    if params is not None:
        '''
        if RUN_TYPE == 'local':
            params_path = os.path.join(LOCAL_REGISTRY_PATH, "params", timestamp + ".pickle")
        elif RUN_TYPE == 'docker':
            params_path = os.path.join("whats_for_dinner/training_outputs/params", timestamp + ".pickle")
        '''
        params_path = os.path.join("whats_for_dinner/training_outputs/params", timestamp + ".pickle")
        print(f"- params path: {params_path}")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # Save metrics
    if metrics is not None:
        '''
        if RUN_TYPE == 'local':
            metrics_path = os.path.join(LOCAL_REGISTRY_PATH, "metrics", timestamp + ".pickle")
        elif RUN_TYPE == 'docker':
            metrics_path = os.path.join("whats_for_dinner/training_outputs/metrics", timestamp + ".pickle")
        '''
        metrics_path = os.path.join("whats_for_dinner/training_outputs/metrics", timestamp + ".pickle")
        print(f"- metrics path: {metrics_path}")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    # Save model
    if model is not None:
        '''
        if RUN_TYPE == 'local':
            model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", timestamp)
        elif RUN_TYPE == 'docker':
            model_path = os.path.join("whats_for_dinner/training_outputs/models", timestamp)
        '''
        model_path = os.path.join("whats_for_dinner/training_outputs/models", timestamp)
        print(f"- model path: {model_path}")
        model.save(model_path)

    print("\n✅ data saved locally")

    return None


def load_model(save_copy_locally=False) -> Model:
    """
    Load the latest saved model, return None if no model found
    """
    # if os.environ.get("MODEL_TARGET") == "mlflow":
    #     stage = "Production"

    #     print(Fore.BLUE + f"\nLoad model {stage} stage from mlflow..." + Style.RESET_ALL)

    #     # load model from mlflow
    #     mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

    #     mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

    #     model_uri = f"models:/{mlflow_model_name}/{stage}"
    #     print(f"- uri: {model_uri}")

    #     try:
    #         model = mlflow.keras.load_model(model_uri=model_uri)
    #         print("\n✅ model loaded from mlflow")
    #     except:
    #         print(f"\n❌ no model in stage {stage} on mlflow")
    #         return None

    #     if save_copy_locally:
    #         from pathlib import Path

    #         # Create the LOCAL_REGISTRY_PATH directory if it does exist
    #         Path(LOCAL_REGISTRY_PATH).mkdir(parents=True, exist_ok=True)
    #         timestamp = time.strftime("%Y%m%d-%H%M%S")
    #         model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", timestamp)
    #         model.save(model_path)

    #     return model

    print(Fore.BLUE + "\nLoad model from local disk..." + Style.RESET_ALL)

    # Get latest model version
    '''
    if RUN_TYPE == 'local':    # version for local machine
        model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
    elif RUN_TYPE == 'docker':     # version for Docker
        model_directory = "whats_for_dinner/training_outputs/models"
    '''
    model_directory = "whats_for_dinner/training_outputs/models"
    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    model_path = sorted(results)[-1]
    print(f"- path: {model_path}")

    model = models.load_model(model_path)
    print("\n✅ model loaded from disk")

    return model


def get_model_version(stage="Production"):
    """
    Retrieve the version number of the latest model in the given stage
    - stages: "None", "Production", "Staging", "Archived"
    """

    # if os.environ.get("MODEL_TARGET") == "mlflow":

    #     mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))

    #     mlflow_model_name = os.environ.get("MLFLOW_MODEL_NAME")

    #     client = MlflowClient()

    #     try:
    #         version = client.get_latest_versions(name=mlflow_model_name, stages=[stage])
    #     except:
    #         return None

    #     # check whether a version of the model exists in the given stage
    #     if not version:
    #         return None

    #     return int(version[0].version)

    # model version not handled

    return None

def save_labels(labels):
    '''
    Save labels to match to output classes
    '''
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    if labels is not None:
        '''
        if RUN_TYPE == 'local':    # version for local machine
            labels_path = os.path.join(LOCAL_REGISTRY_PATH, "labels", timestamp)
        elif RUN_TYPE == 'docker':     # version for Docker
            labels_path = os.path.join("whats_for_dinner/training_outputs/labels", timestamp)
        '''
        labels_path = os.path.join("whats_for_dinner/training_outputs/labels", timestamp)
    np.save(labels_path, labels)


def load_labels():
    '''
    Get labels
    '''
    '''
    if RUN_TYPE == 'local':    # version for local machine
        label_directory = os.path.join(LOCAL_REGISTRY_PATH, "labels")
    elif RUN_TYPE == 'docker':     # version for Docker
        label_directory = "whats_for_dinner/training_outputs/labels"
    '''
    label_directory = "whats_for_dinner/training_outputs/labels"
    results = glob.glob(f"{label_directory}/*")
    labels_path = sorted(results)[-1]
    print(f"- path: {labels_path}")

    labels = np.load(labels_path, allow_pickle=True)
    print("\n✅ labels loaded from disk")

    return labels
