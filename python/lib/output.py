import datetime
import smtplib

def log(file, data):
  now = datetime.datetime.now()
  log = '[' + str(now) + '] ' + str(data) + '\n'
  file.write(log)

def send_email(file, text):
  # set account information
  account = 'xxx'
  password = 'xxx'
  # log out
  log(file, 'text of email: ' + str(text))

  # send email
  server = smtplib.SMTP("smtp.gmail.com", port=587)
  server.ehlo()
  server.starttls()
  server.login(account, password)
  server.sendmail(account, account, text)
