FROM python:3.9.9-slim-bullseye

ENV PROJECT_DIR /app

WORKDIR /app
RUN pip install pipenv

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

WORKDIR ${PROJECT_DIR}
COPY . .

RUN pipenv install --skip-lock
RUN pipenv graph
# RUN pipenv install --system --deploy

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]