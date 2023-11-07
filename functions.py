from elements import links, accounts
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
def max_tries(function, *args) -> None:
    """try to perform a function for MAX_TRIES times"""
    for x in range(MAX_TRIES):
        if function(*args): break
        if x == MAX_TRIES:
            print(f"Tried three times and didn't work")
            raise


def find(element_type, value):
    """Finds the element and returns it, returns None if not found"""
    try:
        element = driver.find_element(by=element_type, value=value)
    except NoSuchElementException:
        message = f"Element {value} does not exist. Current URL: {driver.current_url}"
        add_error(message)
        return None
    except:
        message = f"Unknown error on finding element {value}. Current URL: {driver.current_url}"
        add_error(message)
        return None
    else:
        return element


def btn_click(element):
    """Clicks the indicated element. Error check provided. Doesn't return anythin"""
    try:
        btn = find(*links[element])
        btn.click()
    except ElementClickInterceptedException:
        message = f"Element {element} not clickable. Current URL: {driver.current_url}"
        add_error(message)
        raise
    except:
        message = f"Unknown error on clicking element {element}. Current URL: {driver.current_url}"
        add_error(message)
        traceback.print_exc()
        raise


def box_type(element, value):
    """Types the value in the indicated element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        btn = find(*links[element])
        btn.send_keys(value)
        while btn.get_attribute('value') != value:
            print_to_log(
                f"\t* Little hiccup in box_type func. Value received: {value}, value of input field:{btn.get_attribute('value')}\n\tTrying again...\n")
            btn.clear()
            btn.send_keys(value)
            time.sleep(1)
    except:
        add_error("Couldn't type in the element")
        traceback.print_exc()
        raise


# TODO: change get_month to get_time, with separate variables: year, month, date, hour, minutes, seconds
def get_time():
    """Returns local time (Year, Month, Date, Hour, Minutes, Seconds) as a list"""
    month = int(time.strftime("%m", time.localtime()))
    print(month)
    return month

#TODO: Check the check_url function
def check_url(actual):
    """Checks if you are at the given URL"""

    current_url = driver.current_url
    return current_url == actual

#TODO: Check the sign_ing function
def sign_in(user: str) -> bool:
    """Sign in to the designated user from accounts dictionary. Returns True if
    signed in, returns False in case of error"""
    try:
        btn_click("sign_in_btn")
        box_type("sign_in_mail", accounts[user]["user"])
        box_type("sign_in_pass", accounts[user]["pass"])
        btn_click("sign_in_submit_btn")
        driver.get("http://dev2.tenders.ge/profile/company-info")
        company_name = find(*links["profile_company_name"]).text    # Does it check the sign in? There's no raise
    except:
        return False
    else:
        if company_name == accounts[user]["company_name"]:
            print(f"Signed in successfully to {accounts[user]['user']}")
            return True
        else:
            print(f"The user signed in is not right. User displayed: {company_name}")
            # TODO: Logout

# TODO: URL check test
# TODO: announce tender function


def print_to_log(message):
    try:
        with open("Logs/logs.csv", mode="a", encoding='utf-8') as file:
            print(message)
            file.write(f"{message}\n")
    except:
        with open("Logs/logs.csv", mode="w", encoding='utf-8') as file:
            print(message)
            file.write(f"{message}\n")


