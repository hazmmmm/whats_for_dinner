'''
Module to build, train, evaluate model
'''

from typing import Tuple
import time
from colorama import Fore, Style

print(Fore.BLUE + "\nLoading tensorflow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow.keras import Sequential, layers, Model, optimizers, models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input


end = time.perf_counter()
print(f"\n✅ tensorflow loaded ({round(end - start, 2)} secs)")

def initialize_model(train_df) -> Model:
    '''
    Build and initialize model using a pre-trained model, set its parameters as non-trainable,
    and add additional trainable layers on top
    '''
    model = VGG16(weights="imagenet", include_top=False, input_shape=(224,224,3))

    # Set the first layers to be untrainable
    model.trainable = False

    # Add extra layers
    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(500, activation='relu')
    prediction_layer = layers.Dense(36, activation='softmax')
    model = models.Sequential([
        model,
        flatten_layer,
        dense_layer,
        prediction_layer
    ])
    print("\n✅ model initialized with added last layers")
    return model

def compile_model(model: Model, learning_rate: float) -> Model:
    '''
    Compile model with Adam optimizer
    '''
    opt = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    print("\n✅ model compiled")

    return model

def train_model(model, train_images, val_images, patience, batch_size, epochs) -> Tuple[Model,dict]:
    '''
    Train model using train_ and val_images
    '''
    # Set early stopping
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

    print("\n✅ model trained")

    return model, history

def evaluate_model(model: Model,
                   eval_images) -> Tuple[Model, dict]:
    """
    Evaluate trained model performance on dataset
    """
    print(Fore.BLUE + "\nEvaluating model..." + Style.RESET_ALL)

    if model is None:
        print("\n❌ no model to evaluate")
        return None

    metrics = model.evaluate(eval_images)
    print("✅ model evaluated")

    loss = metrics[0]
    accuracy = metrics[1]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} accuracy {round(accuracy, 2)}")

    return metrics
