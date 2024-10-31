FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./src /src
WORKDIR /src
EXPOSE 8501

ARG DEV=false

RUN apt-get update && \
    apt-get install -y --no-install-recommends cmake g++ gcc && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --no-create-home streamlit-user

ENV PATH="/py/bin:$PATH"

USER streamlit-user

