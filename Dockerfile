# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /code
ENV HOST=mysql
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN python -m pip install --upgrade pip
RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-root
EXPOSE 5000
CMD ["flask", "run"]
