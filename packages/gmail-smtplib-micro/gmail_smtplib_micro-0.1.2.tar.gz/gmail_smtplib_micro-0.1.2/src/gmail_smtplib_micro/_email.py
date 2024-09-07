from ._exceptions import EmailError


class Email():
    subject: str
    body: str

    def __init__(self, subject: str, body: str) -> None:
        if len(subject) < 1:
            raise EmailError("Missing subject text")
        if len(body) < 1:
            raise EmailError("Missing body text")
        self.subject = subject
        self.body = body
