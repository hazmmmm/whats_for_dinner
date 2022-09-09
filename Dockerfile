FROM tensorflow/tensorflow:2.9.1

WORKDIR /prod

COPY whats_for_dinner /whats_for_dinner
# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...

COPY requirements.txt /requirements.txt

RUN pip freeze > requirements.txt

# RUN install -r requirements.txt


# Copy .env with DATA_SOURCE=local and MODEL_TARGET=mlflow
COPY .env .env

# # A build time, download the model from the MLflow server and copy it once for all inside of the image
# RUN python -c 'from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv()); \
#     from whats_for_dinner.ml_logic.registry import load_model; load_model(save_copy_locally=True)'
# # Then, at run time, load the model locally from the container
# # This avoids to download the heavy model from the Internet every time an API request is performed

CMD uvicorn whats_for_dinner.api.fast:app --host 0.0.0.0 --port $PORT
