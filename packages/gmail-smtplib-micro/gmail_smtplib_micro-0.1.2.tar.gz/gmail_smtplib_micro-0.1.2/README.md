# python_snail

Provides a wrapper class for smtplib to handle GMail usage

Set up a configuration file and pass through email data

```python
from gmail_smtplib_micro import GmailSMTPLib

g = GmailSMTPLib("pysnail.conf")
g.send_file("file.email","example@example.com")
```

Can also be invoked with a provided email object

```python
from gmail_smtplib_micro import GmailSMTPLib, Email

subject = "The string of the subject"
body = "This is the body of the email\nIncluding line breaks"

e = Email(subject, body)

g = GmailSMTPLib("pysnail.conf")
g.send_object(e,"example@example.com")
```

Examples of the configuration and email file can be shown via:
```python
from gmail_smtplib_micro import ExampleEmail, ExampleConfiguration

print(ExampleEmail().show())
print(ExampleConfiguration().show())
```
