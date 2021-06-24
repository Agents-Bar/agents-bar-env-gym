FROM python:3.8-slim

# set path to our python api file
ENV MODULE_NAME="app.main"

# Install packages directly here to limit rebuilding on code changes
RUN pip install uvicorn~=0.13.4 fastapi~=0.63.0 pydantic~=1.7.3
RUN pip install requests~=2.25.1
RUN pip install gym~=0.18.0

COPY ./ /app

LABEL agents-bar-env=v0.1.0

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--app-dir", "/app"]
