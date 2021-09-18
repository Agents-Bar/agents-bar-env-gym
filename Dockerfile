FROM python:3.8-slim

# set path to our python api file
ENV MODULE_NAME="app.main"

# TODO: Separate into build stage and move dependencies
RUN apt-get update && apt-get install -y swig gcc g++ cmake zlib1g-dev

WORKDIR /app/agents-bar/env
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ .

LABEL agents-bar-env=v0.2.0

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--app-dir", "/app/agents-bar/env"]
