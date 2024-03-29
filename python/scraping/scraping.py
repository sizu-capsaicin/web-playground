import requests
from bs4 import BeautifulSoup
import time
import smtplib
import datetime
import threading
from lib import output

# URL to scraping
URL = "xxx"
# inform which agent watch site
HEADERS = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
# keywords to check stock
KEYWORD = 'カートに入れる'
# log file path
LOG_PATH = 'xxx'

def check_stock(file):
  # request HTML of the page
  page = requests.get(URL, headers=HEADERS)
  # make BeautifulSoup object
  obj = BeautifulSoup(page.text, 'html.parser')

  # get text of button and check stock of product
  res = obj.find(class_='productDetail--buttons__button--primary js-addToCartButton')
  output.log(file, 'result of obj.find(): ' + str(res))
  if res is not None:
    word = res.get_text()
    output.log(file, 'get word: ' + str(word))
    return (word in KEYWORD)
  
  return False

if __name__ == "__main__":
  with open(LOG_PATH, mode='a') as file:
    check_result = check_stock(file)
    output.log(file, 'result of check_stock(): ' + str(check_result))
    if check_result:
      # set contents of email
      subject = 'Game&Watch arrived'
      text = 'subject:' + subject + '\n\n' + 'It seems that Game&Watch have arrived. ' + '\n' + URL + '\n'
      # send email
      output.send_email(file, text)
