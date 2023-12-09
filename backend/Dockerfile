FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

COPY . /app

CMD ["flask", "run", "--port=5180", "--host=0.0.0.0"]