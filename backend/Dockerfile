FROM python

WORKDIR /app

COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

COPY . /app

CMD ["flask", "run", "--host=0.0.0.0"]