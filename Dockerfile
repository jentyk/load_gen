FROM python:3.11-alpine

ENV PIPENV_VENV_IN_PROJECT=1

RUN addgroup -g 1001 -S lggroup && \
adduser -u 1001 -S lguser -G lggroup

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY load.py ./load.py

USER lguser

ENTRYPOINT ["python", "load.py"]
