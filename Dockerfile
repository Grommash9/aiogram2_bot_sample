FROM python:3.10.8-bullseye

RUN mkdir /telegram_bot

COPY requirements.txt /telegram_bot

RUN python -m pip install -r /telegram_bot/requirements.txt

COPY . /telegram_bot

WORKDIR /telegram_bot

ENTRYPOINT ["python", "-m", "bot_app"]
