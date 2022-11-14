FROM python:3.10.8

# ADD . /code
# WORKDIR /code
# RUN pip install -r requirements.txt
# ENV FLASK_APP=./Backend/app.py
# CMD flask run -p 5001

RUN mkdir -p /app_bucket
WORKDIR /app_bucket

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5004

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get install -y ffmpeg

COPY . .

# ENTRYPOINT [ "flask"]
# CMD [ "run", "--host", "0.0.0.0" ]
#CMD [ "flask", "run"]
CMD [ "flask", "run","-p","5005"]