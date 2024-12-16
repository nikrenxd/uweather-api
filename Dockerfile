FROM python:3.11-alpine

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# env variable for installing dependencies inside container
ENV UV_SYSTEM_PYTHON=1

WORKDIR /usr/app/

# install dependencies
COPY ./pyproject.toml ./uv.lock ./manage.py /usr/app/
RUN uv pip install -r pyproject.toml

COPY ./src/ /usr/app/src/