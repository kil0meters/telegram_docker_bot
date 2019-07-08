FROM python:3-slim

WORKDIR /app

COPY bot.py /app
COPY requirements.txt /app
COPY commands.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV BOT_TOKEN ""
ENV ALLOWED_USERS "" 

CMD ["python3", "bot.py"]
