from elements import links
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time


def init(website):
    """Initialises driver options. Goes to the provided URL"""
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Keep the browser open until .quit command comes
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    driver.implicitly_wait(10)
    return driver


def find(element_type, value):
    """Finds the element and returns it, returns None if not found"""
    try:
        element = driver.find_element(by=element_type, value=value)
    except:
        print("Element does not exist")
        return None
    return element


def btn_click(element):
    """Clicks the indicated element. Error check provided"""

    try:
        btn = find(*links[element])
        btn.click()
    except:
        print("Couldn't click on the element")
        traceback.print_exc()


def box_type(element, value):
    """Types the value in the indicated element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        btn = find(*links[element])
        btn.send_keys(value)
        while btn.get_attribute('value') != value:
            print(btn.text)
            btn.clear()
            btn.send_keys(value)
            time.sleep(1)
    except:
        print("Couldn't type in the element")
        traceback.print_exc()


# TODO: change get_month to get_time, with separate variables: year, month, date, hour, minutes, seconds
def get_time():
    """Returns local time (Year, Month, Date, Hour, Minutes, Seconds) as a list"""
    month = int(time.strftime("%m", time.localtime()))
    print(month)
    return month


def check_url(actual):
    """Checks if you are at the given URL"""

    current_url = driver.current_url
    return current_url == actual


# TODO: Change to dev2
def sign_in(user):
    """Sign in to the designated user"""
    current_url = driver.current_url

# TODO: URL check test
# TODO: announce tender function
