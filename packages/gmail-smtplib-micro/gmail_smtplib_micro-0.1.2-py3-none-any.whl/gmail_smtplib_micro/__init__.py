
from .gmail_smtplib_micro import GmailSMTPLib, MIMEType
from ._examples import ExampleConfiguration, ExampleEmail
from ._email import Email

GmailSMTPLib
MIMEType
ExampleConfiguration
ExampleEmail
Email

VERSION = (0, 1, 2)

VERSION_STRING = '.'.join(map(str, VERSION))
