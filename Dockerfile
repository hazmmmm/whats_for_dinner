# FROM tensorflow/tensorflow:2.9.1
# FROM armswdev/tensorflow-arm-neoverse-n1:r21.12-tf-2.7.0-eigen
FROM python:3.8.12-bullseye

WORKDIR /prod

COPY whats_for_dinner whats_for_dinner
# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...

COPY requirements.txt requirements.txt
COPY setup.py setup.py

# RUN pip freeze > requirements.txt
RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html
RUN pip install -r requirements.txt


# Copy .env with DATA_SOURCE=local and MODEL_TARGET=mlflow
COPY .env .env


CMD uvicorn whats_for_dinner.api.fast:app --host 0.0.0.0 --port $PORT
