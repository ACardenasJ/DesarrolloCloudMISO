const express = require('express');
const nodemailer = require('nodemailer');
const { google } = require('googleapis');
const app = express();

app.use(express.json());

/////
// These id's and secrets should come from .env file.
const CLIENT_ID = '66618618145-pgqktrego6mq1lieom75a118rd1m2gth.apps.googleusercontent.com';
const CLEINT_SECRET = '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';
const REDIRECT_URI = 'https://developers.google.com/oauthplayground';
const REFRESH_TOKEN = '1//04dkT046DM81ACgYIARAAGAQSNwF-L9IrmfHnF0-eI_eG9JMm5B8q6p1FU2sl6MyshGThTNuP9EnvPhwkUUcf2bsZCi52KWlIz4M';

const oAuth2Client = new google.auth.OAuth2(
  CLIENT_ID,
  CLEINT_SECRET,
  REDIRECT_URI
);
oAuth2Client.setCredentials({ refresh_token: REFRESH_TOKEN });

async function sendMail(send_mail, id_task) {
  try {
    const accessToken = await oAuth2Client.getAccessToken();

    const transport = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        type: 'OAuth2',
        user: 'nubedtg23@gmail.com',
        clientId: CLIENT_ID,
        clientSecret: CLEINT_SECRET,
        refreshToken: REFRESH_TOKEN,
        accessToken: accessToken,
      },
    });

    const mailOptions = {
      from: 'SENDER NAME <yours authorised email nubedtg23@gmail.com>',
      to: send_mail, //'jdavidportillam@gmail.com',
      subject: 'Notificacion - CCT G23',
      text: 'Hola, tu archivo ya fue procesado',
      html: '<h1>Hola, tu archivo ya fue procesado con id '+id_task+', ya puedes descargarlo.</h1>',
    };

    const result = await transport.sendMail(mailOptions);
    return result;
  } catch (error) {
    return error;
  }
}
/////






app.get('/', (req, res) => {
    res.send('Hello World - JS');
});
app.get('/api/status', (req, res) => {
    console.log('Status requested');
    //res.send('ok');
    res.json({"status": "ok"});
});

app.post('/api/mail', (req, res) => {
    console.log('POST request received');
    console.log(req.body.mail);
    var mail_send = req.body.mail
    var id_task = req.body.id_task
    console.log(mail_send)
    sendMail(mail_send, id_task)
    .then((result) => console.log('Email sent...', result))
    .catch((error) => console.log(error.message));
    res.json({"status": "ok mail sent"});
});

app.listen(5004, () => {
    console.log('Server is running on port 5004---------------------');
});