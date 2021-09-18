# Build stage
FROM python:3.8-slim as build-stage

RUN apt-get update && apt-get install -y swig gcc g++ cmake zlib1g-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Final stage
FROM python:3.8-slim
COPY --from=build-stage /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

WORKDIR /app/agents-bar/env
COPY ./ .

LABEL agents-bar-env=v0.2.0
ENV MODULE_NAME="app.main"

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--app-dir", "/app/agents-bar/env"]
