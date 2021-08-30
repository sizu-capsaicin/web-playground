from selenium import webdriver
from lib import output
import time

# URL to login
URL_1 = 'xxx'
URL_2 = 'xxx'
URL_3 = 'xxx'
# profile path
USER_DATA_DIR = 'xxx'
PROFILE_PATH = 'xxx'
# URL to check login status
CHECK_LOGIN_URL = URL_3
# class of login button
BEFORE_LOGIN_BUTTON_CLASS = 'xxx'
AFTER_LOGIN_BUTTON_CLASS = 'xxx'
# login form keywords
LOGIN_ID_KEYWORD = 'xxx'
LOGIN_PWD_KEYWORD = 'xxx'
SUBMIT_BUTTON_KEYWORD = 'xxx'
# login info
USER_EMAIL = 'xxx'
USER_PWD = 'xxx'

# URL to check platinum points
POINTS_URL = 'xxx'

# log file path
LOG_PATH = '/Users/sizu/web-playground/python/log/login2.log'

# sleep time
SLEEP_TIME = 5

if __name__ == "__main__":
  # make webdriver object by headless mode
  options = webdriver.ChromeOptions()
  # options.add_argument('--headless')
  options.add_argument('--user-data-dir=' + USER_DATA_DIR)
  options.add_argument('--profile-directory=' + PROFILE_PATH)
  options.add_argument('--lang=jp')
  driver = webdriver.Chrome(options=options)

  # open log file
  with open(LOG_PATH, mode='a') as file:
    # check login status
    driver.get(CHECK_LOGIN_URL)
    output.log(file, 'get CHECK_LOGIN_URL page: title is ' + driver.title)
    button_ary = driver.find_elements_by_class_name(BEFORE_LOGIN_BUTTON_CLASS)
    time.sleep(SLEEP_TIME)

    # if account is not logged in, log in
    if len(button_ary) > 0:
      button = button_ary[0]
      # click login button
      button.click()
      output.log(file, 'get login page: title is ' + driver.title)
      time.sleep(SLEEP_TIME)

      # enter and submit login info
      id_element = driver.find_element_by_id(LOGIN_ID_KEYWORD)
      id_element.clear()
      id_element.send_keys(USER_EMAIL)

      pwd_element = driver.find_element_by_id(LOGIN_PWD_KEYWORD)
      pwd_element.clear()
      pwd_element.send_keys(USER_PWD)
      time.sleep(SLEEP_TIME)

      submit = driver.find_element_by_class_name(SUBMIT_BUTTON_KEYWORD)
      if submit.is_enabled():
        # click submit button
        submit.click()
        time.sleep(SLEEP_TIME * 10)

        # check login status (success or failure)
        button_ary = driver.find_elements_by_class_name(AFTER_LOGIN_BUTTON_CLASS)
        if len(button_ary) > 0:
          output.log(file, 'success to login!: title is ' + driver.title)
        else:
          # send email about login failure
          subject = 'Login Failure Notification!'
          text = 'subject:' + subject + '\n\n' + 'Login failure.\n Submit button is enabled, but could not logged in.'
          output.send_email(file, text)
          exit(1)
      else:
        # send email
        subject = 'login error!'
        text = 'subject:' + subject + '\n\n' + 'Login failure.\n Submit button is not enabled.'
        output.send_email(file, text)
        exit(1)
    
    # get pages
    ary = [URL_1, URL_2, URL_3]
    for url in ary:
      driver.get(url)
      output.log(file, 'get webpage: URL is ' + url)
    
    # check platinum points and send email
    driver.get(POINTS_URL)
    output.log(file, 'get points page: title is ' + driver.title)
    points = driver.find_element_by_class_name('value').text
    
    subject = 'get points'
    text = 'subject:' + subject + '\n\n' + 'This week points: ' + points
    output.send_email(file, text)

  # end of webdriver
  driver.quit()