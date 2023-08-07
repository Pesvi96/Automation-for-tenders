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


def find(element_type: str, value: str) -> WebElement | None:
    """Finds the element and returns it, returns None if not found"""
    try:
        element = driver.find_element(by=element_type, value=value)
    except NoSuchElementException:
        print(f"\t***Element does not exist: {value}***")
        return None
    except ElementNotVisibleException:
        print(f"\t***Element indicated not visible: {value}***")
        return None
    except:
        print(f"\t***Unexpected error with finding element {value}***")
        traceback.print_exc()
        return None
    else:
        return element


def btn_click(element: str) -> None:
    """Clicks the indicated element. Error check provided"""
    try:
        btn = find(*links[element])
        btn.click()
    except:
        print(f"\t***Unexpected error with clicking element {element}***")
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
        print(f"\t***Unexpected error with typing in element {element}***")
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
