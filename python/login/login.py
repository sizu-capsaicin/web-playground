import time
from typing import Tuple
from bs4 import BeautifulSoup
import requests
import datetime

from requests.sessions import session
from lib import output

# inform which agent watch site
HEADERS = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
# URL to check login status
LOGIN_CHECK_URL = "xxx"
# keywords to check login status
USER_NAME = "xxx"

# login form URL
LOGIN_FORM_URL = "xxx"
# mail address to login
EMAIL = 'xxx'
# password to login
PASSWORD = 'xxx'
# redirect URL
REDIRECT_URL = 'xxx'
# redirect after
REDIRECT_AFTER = '5'
# cstf_token
CSTF_TOKEN = 'xxx'

# access page
# 1st page
URL_1 = 'xxx'
# 2nd page
URL_2 = 'xxx'
# 3rd page
URL_3 = 'xxx'

# log file path
LOG_PATH = 'xxx'

def check_login(file):
  # request HTML of the page
  page = requests.get(LOGIN_CHECK_URL, headers=HEADERS)
  # make BeautifulSoup object
  obj = BeautifulSoup(page.text, 'html.parser')

  # get login status
  res = obj.find(class_='nc3-c-gheader-dfHeader__label')
  if res is None:
    # log out 
    output.log(file, 'check_login() cannot get HTML object.')
    # send email
    subject = 'login script error!'
    text = 'subject:' + subject + '\n\n' + 'There was an error in check_login().\n Please check script log.\n'
    output.send_email(file, text)
    exit(1)
  else:
    status = res.get_text()
    output.log(file, 'login status is ' + str(status))
    if status == USER_NAME:
      return True
    else:
      return False

def do_login(file):
  # start session
  session = requests.session()

  # login information
  login_info = {
    'subject_id':EMAIL, 
    'subject_password':PASSWORD, 
    'post_login_redirect_uri':REDIRECT_URL, 
    'redirect_after':REDIRECT_AFTER, 
    'csrf_token':CSTF_TOKEN
  }

  # login action
  res = session.post(LOGIN_FORM_URL, data=login_info)
  result = res.raise_for_status()
  # if result is None, exit script
  if result is not None:
    # log out
    output.log(file, 'do_login() failed to login.')
    # send email
    subject = 'login script error!'
    text = 'subject:' + subject + '\n\n' + 'There was an error in do_login().\n Please check script log.\n'
    output.send_email(file, text)
    exit(1)

def access_page(url):
  # request HTML of the page
  page = requests.get(url, headers=HEADERS)
  # make BeautifulSoup object
  obj = BeautifulSoup(page.text, 'html.parser')

  # log out
  title = obj.find('title').text
  output.log(file, 'result of access_page(): ' + str(title))

if __name__ == "__main__":
  # open log file
  with open(LOG_PATH, mode='a') as file:

    # check login status
    if not check_login(file):
      # if not logined, do login
      do_login(file)

    # access 3 pages
    ary = [URL_1, URL_2, URL_3]
    for url in ary:
      access_page(url)

    # log platinum points
