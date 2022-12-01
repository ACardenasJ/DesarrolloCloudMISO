FROM python:3.10.8
ADD . /code
WORKDIR /code
EXPOSE 8080
RUN pip install -r requirements.txt
CMD ["celery", "-A", "tareas", "worker", "-l", "info", "-P", "solo"]