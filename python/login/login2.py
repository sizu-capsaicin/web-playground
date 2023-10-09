from selenium import webdriver
from selenium.webdriver.common.by import By
# from lib import output
import datetime
import smtplib
import time
import yaml

def load_yml(file_path):
  with open(file_path, 'r') as yml:
    config = yaml.safe_load(yml)
    return config

def log(file, data):
  now = datetime.datetime.now()
  log = '[' + str(now) + '] ' + str(data) + '\n'
  file.write(log)

def send_email(account, pwd, file, text):
  # log out
  log(file, 'text of email: ' + str(text))

  # send email
  server = smtplib.SMTP("smtp.gmail.com", port=587)
  server.ehlo()
  server.starttls()
  server.login(account, pwd)
  server.sendmail(account, account, text)

if __name__ == "__main__":

  config = load_yml('yml/login_config.yml')

  login_urls = config['urls']['login_urls']
  check_login_url = config['urls']['check_login_url']
  points_url = config['urls']['points_url']
  points_history_url = config['urls']['points_history_url']

  user_data_dir = config['chrome_profile']['user_data_dir']
  profile_path = config['chrome_profile']['profile_path']

  before_login_button_class = config['html_elements']['before_login_button_class']
  after_login_button_class = config['html_elements']['after_login_button_class']
  login_form_title = config['html_elements']['login_form_title']
  login_id_keyword = config['html_elements']['login_id_keyword']
  login_pwd_keyword = config['html_elements']['login_pwd_keyword']
  submit_button_keyword = config['html_elements']['submit_button_keyword']

  user_email = config['login_info']['user_email']
  user_pwd = config['login_info']['user_pwd']

  email_account = config['email']['account']
  email_pwd = config['email']['pwd']

  log_path = config['log_path']
  sleep_time = int(config['sleep_time'])

  # make webdriver object by headless mode
  options = webdriver.ChromeOptions()
  # options.add_argument('--headless')
  options.add_argument('--user-data-dir=' + user_data_dir)
  options.add_argument('--profile-directory=' + profile_path)
  options.add_argument('--disable-blink-features=AutomationControlled')
  options.add_argument('--lang=jp')
  driver = webdriver.Chrome(options=options)

  # open log file
  with open(log_path, mode='a') as file:
    # check login status
    driver.get(check_login_url)
    log(file, 'get CHECK_LOGIN_URL page: title is ' + driver.title)
    button_ary = driver.find_elements(By.CLASS_NAME, before_login_button_class)
    time.sleep(sleep_time)

    # if account is not logged in, log in
    if len(button_ary) > 0:
      button = button_ary[0]
      # click login button
      button.click()

      if driver.title == login_form_title:
        log(file, 'get login page: title is ' + driver.title)
        time.sleep(sleep_time)

        # enter and submit login info
        id_element = driver.find_element(By.ID, login_id_keyword)
        id_element.clear()
        id_element.send_keys(user_email)

        pwd_element = driver.find_element(By.ID, login_pwd_keyword)
        pwd_element.clear()
        pwd_element.send_keys(user_pwd)
        time.sleep(sleep_time)

        submit = driver.find_element(By.ID, submit_button_keyword)
        if submit.is_enabled():
          # click submit button
          submit.click()
          time.sleep(sleep_time * 10)

          # check login status (success or failure)
          button_ary = driver.find_elements(By.CLASS_NAME, after_login_button_class)
          if len(button_ary) > 0:
            log(file, 'success to login!: title is ' + driver.title)
          else:
            # send email about login failure
            subject = 'Login Failure Notification!'
            text = 'subject:' + subject + '\n\n' + 'Login failure.\n Submit button is enabled, but could not logged in.'
            send_email(email_account, email_pwd, file, text)
            exit(1)
        else:
          # send email
          subject = 'login error!'
          text = 'subject:' + subject + '\n\n' + 'Login failure.\n Submit button is not enabled.'
          send_email(email_account, email_pwd, file, text)
          exit(1)
    
    # get pages
    for url in login_urls:
      driver.get(url)
      time.sleep(sleep_time)
      # if mynintendo page, click mii icon
      if url == login_urls[2]:
        mii_elements = driver.find_elements(By.CLASS_NAME, "mii")
        # if class name of element, click
        for element in mii_elements:
          if element.get_attribute("class") == "mii":
            element.click()
            time.sleep(sleep_time)
      log(file, 'get webpage: URL is ' + url)
    
    # check platinum points and send email
    driver.get(points_url)
    log(file, 'get points page: title is ' + driver.title)
    points = driver.find_element(By.CLASS_NAME, 'value').text
    
    subject = 'get points'
    text = 'subject:' + subject + '\n\n' + 'This week points: ' + points
    send_email(email_account, email_pwd, file, text)

    driver.get(points_history_url)
    time.sleep(10)

  # end of webdriver
  driver.quit()