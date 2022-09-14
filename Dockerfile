FROM tensorflow/tensorflow:2.9.1
# FROM armswdev/tensorflow-arm-neoverse-n1:r21.12-tf-2.7.0-eigen


WORKDIR /prod
COPY whats_for_dinner whats_for_dinner
# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...

COPY requirements.txt requirements.txt
COPY setup.py setup.py

# RUN pip freeze > requirements.txt

## for Macbook
# RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html

RUN pip install --upgrade pip
## for non-Macbook


RUN pip install .

# Copy .env with DATA_SOURCE=local and MODEL_TARGET=mlflow
COPY .env .env

RUN python -c 'from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv()); \
    from whats_for_dinner.ml_logic.registry import load_model; load_model(save_copy_locally=True)'
# Then, at run time, load the model locally from the container instead of querying the MLflow server, thanks to "MODEL_TARGET=local"

CMD MODEL_TARGET=local uvicorn whats_for_dinner.api.fast:app --host 0.0.0.0 --port $PORT
