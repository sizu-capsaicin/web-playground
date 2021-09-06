from lib import output

# log file path
LOG_PATH = '/Users/sizu/web-playground/python/log/login2.log'

if __name__ == "__main__":
  # send email to run python script
  with open(LOG_PATH, mode='a') as file:
    subject = 'New week started!'
    text = 'subject:' + subject + '\n\n' + 'Today is Monday.\nYou must run login2.py!!!'
    output.send_email(file, text)