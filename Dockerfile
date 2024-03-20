FROM python:3.10-slim

RUN pip install pipenv

WORKDIR /idoven
RUN mkdir ./db
COPY . .

RUN ["pipenv", "install", "--system", "--deploy", "--dev"]
RUN ["alembic", "upgrade", "head"]

EXPOSE 80
ENV APP_CONFIG_FILE=local
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
