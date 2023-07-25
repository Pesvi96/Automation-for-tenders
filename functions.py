from elements import links
from selenium import webdriver
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import traceback
import time

MAX_TRIES = 3


def init(website: str) -> object:
    """Initialises driver options. Goes to the provided URL"""
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Keep the browser open until .quit command comes
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    driver.implicitly_wait(10)
    return driver


# TODO: Should it return None?
def max_function_tries(function) -> None:
    """try to perform a function for MAX_TRIES times"""
    for x in range(MAX_TRIES):
        if function(): break
        if x == MAX_TRIES:
            print(f"Tried three times and didn't work")


def find(element_type: str, value: str) -> WebElement | None:
    """Finds the element and returns it, returns None if not found"""
    try:
        element = driver.find_element(by=element_type, value=value)
        print(type(element))
    except NoSuchElementException:
        print("Element does not exist")
        return None
    except ElementNotVisibleException:
        print("Element indicated not visible")
        return None
    else:
        return element


def btn_click(element: str) -> None:
    """Clicks the indicated element. Error check provided"""
    try:
        btn = find(*links[element])
        btn.click()
    except:
        print("Couldn't click on the element")
        traceback.print_exc()
        raise


def box_type(element: str, value: str) -> None:
    """Types the value in the indicated element. Checks if the value in
    the element is right after typing. Raises error if 3 tries of
    typing was not enough. Error check provided"""
    try:
        btn = find(*links[element])
        btn.send_keys(value)
        count = 0
        while btn.get_attribute('value') != value:
            print(btn.text)
            btn.clear()
            btn.send_keys(value)
            time.sleep(1)
            count += 1
            if count == MAX_TRIES:
                raise
    except:
        print("Couldn't type in the element")
        traceback.print_exc()
        raise


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
def sign_in():
    """Sign in to the designated user"""
    btn_click("announce_btn")

# TODO: URL check test
# TODO: announce tender function
