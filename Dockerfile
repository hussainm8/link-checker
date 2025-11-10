FROM python:3.10-slim
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app