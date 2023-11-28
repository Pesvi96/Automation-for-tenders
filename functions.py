from elements import links, accounts
from selenium import webdriver
# from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    ElementClickInterceptedException
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
    driver.implicitly_wait(15)
    global wait
    wait = WebDriverWait(driver, 10)
    return driver


# def max_tries(function, *args) -> None:
#     """try to perform a function for MAX_TRIES times"""
#     for x in range(MAX_TRIES):
#         if function(*args): break
#         if x == MAX_TRIES:
#             print(f"Tried three times and didn't work")
#             raise


def find(element_name: str) -> object:
    """Receives string for element_name. Finds the element parameters in elements
    dictionary and returns WebElement object, returns None if not found"""
    try:
        element_type, element_value = links[element_name]
        element = driver.find_element(by=element_type, value=element_value)
    except NoSuchElementException:
        print_to_log(f"Element {element_name} does not exist. Current URL: {driver.current_url}")
        return None
    except Exception as err:
        print_to_log(
            f"Unknown error on finding element {element_name}. Current URL: {driver.current_url}. Error: {err}")
        return None
    else:
        return element


def btn_click(element: str) -> None:
    """Clicks the indicated element. Receives name of the element from links dictionary.
     Error check provided. Doesn't return anything"""
    try:
        btn = find(element)
        btn.click()
    except ElementClickInterceptedException:
        print_to_log(f"Element {element} not clickable. Current URL: {driver.current_url}")
        raise
    except Exception as err:
        print_to_log(f"Unknown error on clicking element {element}. Current URL: {driver.current_url}. Error: {err}")
        raise


def box_type(element: str, value: str) -> None:
    """Types the value in the indicated element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        btn = find(element)
        btn.send_keys(value)
        while btn.get_attribute('value') != value:
            print_to_log(
                f"\t* Little hiccup in box_type func. Value received: {value}, value of input field:{btn.get_attribute('value')}\n\tTrying again...\n")
            btn.clear()
            btn.send_keys(value)
            time.sleep(1)
    except Exception as err:
        print_to_log(f"Unknown error with box_type func. Couldn't type in the element. Error: {err}")
        raise


def mce_type(element: str, value: str):
    """Type the value in the indicated TinyMCE element. Checks if the value in
    the element is right after typing. Error check provided"""
    input("Let's pretend you have written this functino. Write something in the cursed mce and continue with 'Enter'")


# TODO: change get_month to get_time, with separate variables: year, month, date, hour, minutes, seconds
def get_time():
    """Returns local time (Year, Month, Date, Hour, Minutes, Seconds) as a list"""
    month = int(time.strftime("%m", time.localtime()))
    print_to_log(month)
    return month


def check_url(actual):
    """Checks if you are at the given URL"""

    current_url = driver.current_url
    return current_url == actual


def print_to_log(message):
    try:
        with open("Logs/logs.txt", mode="a", encoding='utf-8') as file:
            print(message)
            file.write(f"{message}\n")
    except:
        with open("Logs/logs.txt", mode="w", encoding='utf-8') as file:
            print(message)
            file.write(f"{message}\n")


""" Code above is general, not specified for this web automation """


def sign_in(user: str) -> bool:
    """Sign in to the designated user from accounts dictionary. Returns True if
    signed in, returns False in case of error"""
    try:
        an_reg_btn = find("announce/register_btn")
        if an_reg_btn.text == "გამოცხადება":
            print_to_log("Already signed in. Signing out")
            sign_out()
        btn_click("sign_in_btn")
        box_type("sign_in_mail", accounts["dev2"][user]["user"])
        box_type("sign_in_pass", accounts["dev2"][user]["pass"])
        btn_click("sign_in_submit_btn")
        driver.get("http://dev2.tenders.ge/profile/company-info")
        company_name = find("profile_company_name").text  # Does it check the sign in? There's no raise
    except Exception as err:
        print_to_log(f"Unknown error with sign_in func. Error: {err}")
        return False
    else:
        if company_name == accounts["dev2"][user]["company_name"]:
            print_to_log(f"Signed in successfully to {accounts["dev2"][user]["company_name"]}")
            return True
        else:
            print_to_log(f"The user signed in is not right. User displayed: {company_name}")


def sign_out() -> None:
    """Signs out from present account. Doesn't return anything """
    try:
        btn_click("company_dropdown_list")
        btn_click("sign_out_btn")
    except Exception as err:
        print_to_log(f"Unknown error with sign_out func. Error: {err}")
    else:
        print_to_log("Signed out successfully")


def add_tender(tender_type: str, closed: bool, price_list: bool, custom_fields: bool,
               invitations: bool, inv_company_list: list, transportation: bool) -> str:
    """Receives params to check which type tender you want. Returns created tender ID.
    tender_type: e-tender / spot (announcement not needed)
    closed: True / False
    price_list: True / False
    custom_fields: True / False
    invitations: True / False
    inv_company_list: list of dict?
    transportation: True / False
    """

    pass


def e_tender():
    pass


def spot():
    pass


def category():
    pass


def price_list():
    pass


def custom_fields():
    pass


def invite_companies():
    pass

# TODO: URL check test
