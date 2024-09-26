FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry

RUN poetry install --without dev


# Copy the project code into the container
COPY . /app/
