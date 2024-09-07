import smtplib

from enum import Enum
from email.mime.text import MIMEText

from ._utils import read_file
from ._exceptions import ConfigurationError, EmailError
from ._email import Email


class MIMEType(Enum):
    PLAIN = 'plain'
    HTML = 'html'


class GmailSMTPLib():

    _conf_file: str
    _conf_data: list[str]

    _email_file: str
    _email_data: list[str]

    _email: Email

    _sender: str
    _app_pass: str

    def __init__(self, configuration_file: str) -> None:
        self._conf_file = configuration_file
        res = self._validate_conf()
        if not res:
            raise ConfigurationError(
                "Failed to parse provided configuration file - Unknown error")

    def _validate_conf(self) -> bool:
        conf_data = read_file(self._conf_file)
        if conf_data is False:
            raise ConfigurationError("Failed to read file")
        if len(conf_data) != 2:
            raise ConfigurationError(
                "Configuration file should only contain `sender` and `password`")
        conf_data[0] = conf_data[0].split('=', 1)
        conf_data[1] = conf_data[1].split('=', 1)
        if len(conf_data[0]) != 2:
            raise ConfigurationError("Missing sender separator")
        if len(conf_data[1]) != 2:
            raise ConfigurationError("Missing password separator")
        conf_data[0] = conf_data[0][1]
        conf_data[1] = conf_data[1][1]
        if len(conf_data[0]) < 1:
            raise ConfigurationError("Missing sender value")
        if len(conf_data[1]) < 1:
            raise ConfigurationError("Missing password value")
        self._conf_data = conf_data
        return True

    def _validate_email(self) -> bool:
        email_data = read_file(self._email_file)

        if email_data is False:
            raise EmailError(
                "Failed to parse provided email file - Unknown error")

        if len(email_data) < 2:
            raise EmailError("Email file should contain at least 2 lines")

        email_data[0] = email_data[0].split('=', 1)
        email_data[1] = email_data[1].split('=', 1)

        if len(email_data[0]) != 2:
            raise EmailError("Missing subject separator")
        if len(email_data[1]) != 2:
            raise EmailError("Missing body separator")

        email_data[0] = email_data[0][1]
        email_data[1] = email_data[1][1] + '\n' + "\n".join(email_data[2:])

        if len(email_data[0]) < 1:
            raise EmailError("Missing subject text")
        if len(email_data[1]) < 1:
            raise EmailError("Missing body text")
        self._email = Email(email_data[0], email_data[1])
        return True

    def send_object(self, email_obj: Email, recipient: str, mimetype: MIMEType = MIMEType.PLAIN):
        self._email = email_obj
        self._email_data = [self._email.subject, self._email.body]

        self._send(recipient, mimetype)

    def send_file(self, email_file: str, recipient: str, mimetype: MIMEType = MIMEType.PLAIN):
        self._email_file = email_file
        res = self._validate_email()
        if not res:
            return

        self._send(recipient, mimetype)

    def _send(self, recipient, mimetype: MIMEType = MIMEType.PLAIN):
        sender = self._conf_data[0]
        password = self._conf_data[1]

        subject = self._email.subject
        body = self._email.body
        msg = MIMEText(body, _subtype=mimetype.value)
        msg['Subject'] = subject
        msg['From'] = self._conf_data[0]
        msg['To'] = recipient
        # print(msg)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient, msg.as_string())
