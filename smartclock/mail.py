import ssl
import smtplib
from email.mime.text import MIMEText
from flask import render_template
from bs4 import BeautifulSoup


# Basic Example | Unrestricted Local SMTP Server
class BasicEmail():
    # Create the Message
    msg = MIMEText("textbody")
    msg["Subject"] = 'subject'
    msg["From"] = 'sender'
    msg["To"] = 'recipient'

    # Send Message
    context = ssl.create_default_context()
    server, port = "127.0.0.1", 25
    with smtplib.SMTP_SSL(server, port, context=context) as s:
        s.sendmail('sender', 'recipient', msg.as_string())

# HTML Example | Unrestricted Local SMTP Server
class HttpEmail():
    # Create the Message
    msg = MIMEText("alternative")
    msg["Subject"] = 'subject'
    msg["From"] = 'sender@email.com'
    msg["To"] = 'recipient@email.com'

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText('text_body', "plain")
    part2 = MIMEText('html_body', "html")

    # Send Message
    context = ssl.create_default_context()
    server, port = "127.0.0.1", 25
    with smtplib.SMTP_SSL(server, port, context=context) as s:
        s.sendmail('sender', 'recipient', msg.as_string())

# Password Restricted SMTP Server
class SMTPEmail():
    # Create the Message
    msg = MIMEText("alternative")
    msg["Subject"] = 'subject'
    msg["From"] = 'sender@email.com'
    msg["To"] = 'recipient@email.com'

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText('text_body', "plain")
    part2 = MIMEText('html_body', "html")

    # Send Message
    context = ssl.create_default_context()
    server, port = "127.0.0.1", 25
    with smtplib.SMTP_SSL(server, port, context=context) as s:
        s.login('sender s email', 'password')
    s.sendmail('sender@email.com', 'recipient@email.com', msg.as_string())


class HttpEmailWithTemplate():

    # Create the Message
    msg = MIMEText("alternative")
    msg["Subject"] = 'subject'
    msg["From"] = 'sender@email.com'
    msg["To"] = 'recipient@email.com'

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText('text_body', "plain")
    html_body = render_template("email_template.html", user={'name':'silom'})
    part2 = MIMEText(html_body, "html")

    # Send Message
    context = ssl.create_default_context()
    server, port = "127.0.0.1", 25
    with smtplib.SMTP_SSL(server, port, context=context) as s:
        s.sendmail('sender@email.com', 'recipient@email.com', msg.as_string())



html_body = render_template("email_template.html", user={'name':'silom'})
soup = BeautifulSoup(html_body, "html.parser") # removes html tags
text_body = " ".join(soup.text.strip().split())
