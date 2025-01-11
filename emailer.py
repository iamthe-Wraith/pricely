import smtplib

class Emailer:
    def __init__(self, smtp_email: str, smtp_token: str, smtp_host: str, smtp_port: int):
        self.smtp_email = smtp_email
        self.smtp_token = smtp_token
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

        self._validate_config()

    def send_email(self, to: str, from_: str, subject: str, body: str):
        try:                
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as connection:
                connection.starttls() # IMPORTANT: secures the connection with tls
                connection.login(user=self.smtp_email, password=self.smtp_token)
                connection.sendmail(
                    from_addr=self.smtp_email,
                    to_addrs=to,
                    msg=f"Subject:{subject}\n\n{body}"
                )
        except Exception as e:
            print(f"Error sending flight data: {e}")

    def _validate_config(self):
        if not self.smtp_email:
            raise ValueError("SMTP email is required")
        if not self.smtp_token:
            raise ValueError("SMTP token is required")
        if not self.smtp_host:
            raise ValueError("SMTP host is required")
        if not self.smtp_port:
            raise ValueError("SMTP port is required")

