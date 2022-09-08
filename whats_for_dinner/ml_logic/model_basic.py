from colorama import Fore, Style
from typing import Tuple

import time
print(Fore.BLUE + "\nLoading tensorflow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow.keras import Sequential, layers, Model, optimizers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers.experimental.preprocessing import Rescaling

end = time.perf_counter()
print(f"\n✅ tensorflow loaded ({round(end - start, 2)} secs)")

def initialize_model(train_df) -> Model:

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

    return model

def compile_model(model: Model, learning_rate: float) -> Model:

    opt = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

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
    return model, history

def evaluate_model(model: Model,
                   eval_images,
                   batch_size=64) -> Tuple[Model, dict]:
    """
    Evaluate trained model performance on dataset
    """

    print(Fore.BLUE + f"\nEvaluating model..." + Style.RESET_ALL)

    if model is None:
        print(f"\n❌ no model to evaluate")
        return None

    metrics = model.evaluate(
        eval_images,
        batch_size=batch_size,
        verbose=1,
        # callbacks=None,
        return_dict=True)

    loss = metrics["categorical_crossentropy"]
    accuracy = metrics["accuracy"]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} accuracy {round(accuracy, 2)}")

    return metrics
