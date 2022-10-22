from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
import smtplib, ssl





class VistaEnviarCorreo(Resource):

    def enviar_correo(self, sender_email):
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "acj8991@gmail.com"
        receiver_email = sender_email
        password = "1213456"
        message = """\
        Subject: Hi there

        Su archivo fue realizado exitosamante."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
