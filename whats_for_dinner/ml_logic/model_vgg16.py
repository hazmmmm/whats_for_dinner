from colorama import Fore, Style
from typing import Tuple

import time
print(Fore.BLUE + "\nLoading tensorflow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow.keras import Sequential, layers, Model, optimizers, models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input


end = time.perf_counter()
print(f"\n✅ tensorflow loaded ({round(end - start, 2)} secs)")

def initialize_model(train_df) -> Model:

    model = VGG16(weights="imagenet", include_top=False, input_shape=(224,224,3))
    #model.add(Rescaling(1./255, input_shape=(224,224,3))) do we need this Hazm?

    # Set the first layers to be untrainable
    model.trainable = False

    print("\n✅ model initialized")

    return model

def add_last_layers(model):
    '''Take a pre-trained model, set its parameters as non-trainable, and add additional trainable layers on top'''

    base_model = set_nontrainable_layers(model)
    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(500, activation='relu')
    prediction_layer = layers.Dense(36, activation='softmax')


    model = models.Sequential([
        base_model,
        flatten_layer,
        dense_layer,
        prediction_layer
    ])
    print("\n✅ model with added last layers")

    return model

def compile_model(model: Model, learning_rate: float) -> Model:

    opt = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    print("\n✅ model compiled")

    return model

def train_model(model, train_images, val_images, patience, batch_size, epochs) -> Tuple[Model,dict]:

    es = EarlyStopping(monitor = 'val_accuracy',
                    mode = 'max',
                    patience = patience,
                    verbose = 1,
                    restore_best_weights = True)

    history = model.fit(train_images,
                                validation_data = val_images,
                                batch_size = batch_size,
                                epochs = epochs,
                                callbacks=[es])

    print(f"\n✅ model trained")

    return model, history

def evaluate_model(model: Model,
                   eval_images) -> Tuple[Model, dict]:
    """
    Evaluate trained model performance on dataset
    """

    print(Fore.BLUE + f"\nEvaluating model..." + Style.RESET_ALL)

    if model is None:
        print(f"\n❌ no model to evaluate")
        return None

    metrics = model.evaluate(eval_images)
    print("Model evaluated")

    loss = metrics[0]
    accuracy = metrics[1]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} accuracy {round(accuracy, 2)}")

    return metrics
