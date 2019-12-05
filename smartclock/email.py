import requests
from flask_mail import Mail, Message
from smartclock import mail

def send_email(to, subject, template):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox66b2b3ffeee94ac996235293789ac4a9.mailgun.org/messages",
		auth=("api", "20969a1accac0ace6dddc07376f98ae3-e470a504-74e079fc"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox66b2b3ffeee94ac996235293789ac4a9.mailgun.org>",
			"to": to,
			"subject": subject,
			"html": template})


def send_email2(to, subject, template):

	msg = Message(subject=subject,
	    recipients=[to],
	    html = template)
	mail.send(msg)

	return 'message is sent'