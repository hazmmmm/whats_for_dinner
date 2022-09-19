'''
Module defining rudimentary Conv2D model
'''

import time
from typing import Tuple
from colorama import Fore, Style

print(Fore.BLUE + "\nLoading tensorflow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow.keras import Sequential, layers, Model, optimizers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers.experimental.preprocessing import Rescaling

end = time.perf_counter()
print(f"\n✅ tensorflow loaded ({round(end - start, 2)} secs)")

def initialize_model(train_df) -> Model:
    '''
    Building the Conv2D model and returning a model
    '''

    model = Sequential()
    model.add(Rescaling(1./255, input_shape=(224,224,3)))

    model.add(layers.Conv2D(32, kernel_size=3, activation='relu', padding='same'))
    model.add(layers.MaxPooling2D(2, padding='same'))

    model.add(layers.Conv2D(32, kernel_size=3, activation="relu", padding='same'))
    model.add(layers.MaxPooling2D(2, padding='same'))
    model.add(layers.Dropout(0.2))

    model.add(layers.Conv2D(64, kernel_size=3, activation="relu", padding='same'))
    model.add(layers.MaxPooling2D(2, padding='same'))
    model.add(layers.Dropout(0.2))

    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(len(train_df.Label.unique()), activation='softmax'))

    print("\n✅ model initialized")

    return model

def compile_model(model: Model, learning_rate: float) -> Model:
    '''
    Compiling the model with Adam optimizer, checking accuracy
    '''

    opt = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    print("\n✅ model compiled")

    return model

def train_model(model, train_images, val_images, patience, batch_size, epochs) -> Tuple[Model,dict]:
    '''
    Training the model
    '''
    # Define EarlyStopping
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
    print("Model evaluated")

    loss = metrics[0]
    accuracy = metrics[1]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} accuracy {round(accuracy, 2)}")

    return metrics
