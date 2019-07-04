FROM python:3-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV API_TOKEN ""

CMD ["python3", "app.py"]
