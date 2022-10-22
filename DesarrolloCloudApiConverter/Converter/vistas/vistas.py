from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
import json
from sqlalchemy import desc
import smtplib, ssl

from celery import Celery







class VistaConvertir(Resource):

  

   
    def post(self):
       pass

    def enviar_correo():
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "my@gmail.com"
        receiver_email = "your@gmail.com"
        password = input("Type your password and press enter:")
        message = """\
        Subject: Hi there

        This message is sent from Python."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
