import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart('alternative')
msg['Subject'] = f'Список вакансий за {today}'
msg['From'] = EMAIL_HOST_USER
mail = smtplib.SMTP()
mail.connect(EMAIL_HOST, 25)
mail.ehlo()
mail.starttls()
mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

html_m = '<h1>Hello</h1>'
part = MIMEText(html_m, 'html')
msg.attach(part)
mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
mail.quit()