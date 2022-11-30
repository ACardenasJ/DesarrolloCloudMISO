FROM python:3.10.8

RUN mkdir -p /app_api
WORKDIR /app_api

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV PYTHONPATH "${PYTHONPATH}:/app_api"
ENV PYTHONUNBUFFERED 1

EXPOSE 8080

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", ":8080", "--timeout", "300"]