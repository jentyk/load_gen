FROM python:3.11-alpine

ENV PIPENV_VENV_IN_PROJECT=1

RUN addgroup -g 1001 -S naapgroup && \
adduser -u 1001 -S naapuser -G naapgroup

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY load.py ./load.py

USER naapuser

ENTRYPOINT ["python", "load.py"]
