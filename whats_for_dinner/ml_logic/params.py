"""
whats_for_dinner model package params
load and validate the environment variables in the `.env`
"""

import os
import numpy as np

# run type
RUN_TYPE = os.environ.get("RUN_TYPE")

# filepaths
if RUN_TYPE == 'local':
    LOCAL_DATA_PATH = os.path.join(os.environ.get("LOCAL_DATA_PATH"),"fruits_and_vegetables_image_recognition_dataset") #test
else:
    LOCAL_DATA_PATH = ""

LOCAL_REGISTRY_PATH = os.environ.get("LOCAL_REGISTRY_PATH")

# model params
LEARNING_RATE = 0.0001
BATCH_SIZE = 32
EPOCHS = 100
PATIENCE =  6
