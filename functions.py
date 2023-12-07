from datetime import datetime
from elements import links, accounts
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    ElementClickInterceptedException
import traceback
import time
import re

driver: WebDriver
env_accounts: dict
wait: WebDriverWait
env: str
action: ActionChains
MAX_TRIES = 3


# count = 0


def init(website: str, test_env=True, count=0) -> WebDriver:
    """Initialises driver options. Goes to the provided URL"""
    global driver, wait, env, env_accounts, action
    if test_env:
        env = "http://dev2."
        env_accounts = accounts["dev2"]
    else:
        env = "https://"
        env_accounts = accounts["main"]
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Keep the browser open until .quit command comes
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(env + website)
    except Exception as err:
        print_to_log(f"Error with init func. Trying again. error: {err}")
        count += 1
        if count == MAX_TRIES:
            print_to_log(f"Function init failed after {MAX_TRIES} times. Shutting down")
            exit()
        init(website, test_env, count)
    return driver


def find(element_name: str) -> WebElement | None:
    """Receives string for element_name. Finds the element parameters in elements
    dictionary and returns WebElement object, returns None if not found"""
    try:
        element_type, element_value = links[element_name]
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((element_type, element_value)))
        element = driver.find_element(by=element_type, value=element_value)
    except NoSuchElementException:
        print_to_log(f"Element {element_name} does not exist. Current URL: {driver.current_url}.")
        return None
    except Exception as err:
        print_to_log(
            f"Error with find func. Looking for: {element_name}. Current URL: {driver.current_url}. Error: {err}.")
        return None
    else:
        return element


def btn_click(element_name: str) -> None:
    """Clicks the indicated element. Receives name of the element from links dictionary.
     Error check provided. Doesn't return anything"""
    try:
        btn = find(element_name)
        btn.click()
    except ElementClickInterceptedException:
        print_to_log(f"Element {element_name} not clickable. Current URL: {driver.current_url}")
        raise
    except Exception as err:
        print_to_log(
            f"Error with btn_click func. Element_name {element_name}. Current URL: {driver.current_url}. Error: {err}")
        raise


def box_type(element_name: str, value: str) -> None:
    """Types the value in the indicated element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        element = find(element_name)
        element.send_keys(value)
        if element.get_attribute('value') != None:
            element_value = element.get_attribute('value')
            print_to_log("box_type func. Tried value for check")
        elif element.get_attribute('textContent') != None:
            element_value = element.get_attribute('textContent')
            print_to_log("box_type func. Tried textContent for check")
        else:
            element_value = element.text
            print_to_log("box_type func. Tried .text for check")

        if element_value != value:
            for x in range(3):
                print_to_log(
                    f"\t* Little hiccup in box_type func. Value received: {value}, value of input field:{element_value}\n\tTrying again...\n")
                element.clear()
                element.send_keys(value)
                time.sleep(1)
                if element_value == value:
                    break
                if x == 2:
                    raise Exception("Tried 3 times to type in box, didn't work")
    except Exception as err:
        print_to_log(f"Error with box_type func. Element name: {element_name}. Error: {err}")
        raise


def mce_type(element_name: str, value: str) -> None:
    """Types the value in the indicated TinyMCE element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        mce = find(element_name)
        driver.switch_to.frame(mce)
        box_type("announce_tender_description_input_body", value)
        driver.switch_to.default_content()
    except Exception as err:
        print_to_log(f"Error with mce_Type func. Error: {err}")
    else:
        print_to_log("MCE Typed successfully")


def get_submission_deadline() -> str:
    """Returns local time (Year, Month, Date, Hour, Minutes, Seconds) as a dictionary"""
    now = datetime.now()
    if now.minute > 55:
        now = now.replace(hour=now.hour + 1, minute=5 - (60 - now.minute))
    else:
        now = now.replace(minute=now.minute + 5)
    return now.strftime("%Y-%m-%d %H:%M")


def check_url(actual) -> bool:
    """Checks if you are at the given URL. Returns bool"""

    current_url = driver.current_url
    return current_url == actual


def print_to_log(message) -> None:
    """Prints to log.txt. Starts from a clear page on every execution"""
    try:
        with open("Logs/logs.txt", mode="a", encoding='utf-8') as file:
            print(message)
            file.write(f"{message}\n")
    except:
        with open("Logs/logs.txt", mode="w", encoding='utf-8') as file:
            print(message)
            file.write(f"{message}\n")


def select_unit(element_name: str, index: int, count=0) -> None:
    """Selects desired index from the drop-down list and checks (3 times) if it's selected"""
    unit = find(element_name)
    select = Select(unit)
    try:
        select.select_by_index(index)
    except Exception as err:
        print_to_log(f"Error with select_unit func. Trying again. error: {err}")
    if unit.get_attribute('value') == str(index):
        print_to_log("Attribute right, leaving select_unit func")
    elif count == MAX_TRIES:
        print_to_log(f"select_unit func: {MAX_TRIES} tries reached. Exiting func")
    else:
        print_to_log(f"Attribute not right, trying again. Attribute: {unit.get_attribute('value')}."
                     f" Type: {type(unit.get_attribute('value'))}")
        count += 1


def calendar_input(element_name: str, value: str, count=0) -> None:
    """Sets Calendar date/time according to this format: 2023-11-30 18:00"""
    calendar = find(element_name)
    try:
        driver.execute_script("arguments[0].value=arguments[1];", calendar, value)
    except Exception as err:
        print_to_log(
            f"Error with calendar_input func. Element received: {element_name}, value received {value}. Error: {err}")
    calendar_value = calendar.get_attribute('value')
    if calendar_value == value:
        print_to_log("Calendar_input func worked successfully")
    elif count == MAX_TRIES:
        print_to_log(f"Calendar_input: {MAX_TRIES} tries reached. Exiting func")
    else:
        print_to_log(f"Incorrect input in calendar_input func. Element received: {element_name},"
                     f" Value received {value}, existing value {calendar_value}")
        count += 1
        calendar_input(element_name, value, count)


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
        box_type("sign_in_mail", env_accounts[user]["mail"])
        box_type("sign_in_pass", env_accounts[user]["pass"])
        btn_click("sign_in_submit_btn")
        driver.get(f"{env}tenders.ge/profile/company-info")
        company_name = find("profile_company_name").text  # Does it check the sign in? There's no raise
    except Exception as err:
        print_to_log(f"Error with sign_in func. Error: {err}")
        return False
    else:
        if company_name == env_accounts[user]["company_name"]:
            print_to_log(f"Signed in successfully to {env_accounts[user]["company_name"]}")
            return True
        else:
            print_to_log(f"The user signed in is not right. User displayed: {company_name}. Trying again")
            sign_in(user)


def sign_out() -> None:
    """Signs out from present account. Doesn't return anything """
    try:
        btn_click("company_dropdown_list")
        btn_click("sign_out_btn")
    except Exception as err:
        print_to_log(f"Error with sign_out func. Error: {err}")
    else:
        print_to_log("Signed out successfully")


class Tender():

    def __init__(self, is_spot=False, is_closed=True, has_price_list=False, has_custom_fields=False,
                 has_invitations=False, is_transportation=False):
        """Creates an open E-Tender without Price List and has_invitations as a default"""
        self.is_spot = is_spot
        self.is_closed = is_closed
        self.has_price_list = has_price_list
        self.has_custom_fields = has_custom_fields
        self.has_invitations = has_invitations
        self.is_transportation = is_transportation

    def add_tender(self) -> str:
        """
        Receives params to check which type tender you want. Returns created tender ID.
        is_spot: True / False (SPOT if true, E-Tender if False, announcement not needed)
        is_closed: True / False
        has_price_list: True / False
        has_custom_fields: True / False
        has_invitations: True / False
        inv_company_list: list of dict? ???????????
        is_transportation: True / False
        """
        sign_in("announcer")
        btn_click("announce/register_btn")
        if self.is_spot:
            self.add_spot_general_info()
        else:
            self.add_etender_general_info()
        box_type("announce_tender_title_input", "Automation Tender")
        mce_type("announce_tender_description_input", "test")
        box_type("announce_tender_email_input", env_accounts["announcer"]["mail"])
        btn_click("add_tender_btn_class")
        if self.is_spot == False:
            self.indicate_cpv_category()
        btn_click("add_tender_btn_class")
        if self.has_invitations == True:
            self.invite_companies()
        print_to_log("Looking for next button in invitations page")
        btn_click("add_tender_btn_class")
        tender_full_name = find("announcer_tender_preview_title").get_attribute('textContent')
        tender_id = str(re.findall('[S|T]([0-9]+)', tender_full_name))
        print_to_log(f"Tender ID: {tender_id}")
        # btn_click("announcer_tender_preview_submit_btn")
        if self.is_spot == False:
            self.approve_tender_admin(tender_id)
        return tender_id
        # Categories here for e_tenders

    def add_etender_general_info(self) -> None:
        btn_click("announce_etender_btn")
        if self.is_transportation:
            transportation_btn = find("announce_tender_transportation_yes_btn")
            driver.execute_script("arguments[0].click();", transportation_btn)
            price_list_btn = find(
                "announce_tender_price_list_btn")  # Somehow clicking transportation radio locks price list
            # button, next line is for that
            driver.execute_script("arguments[0].classList.remove('btn-disabled');", price_list_btn)
            print_to_log("Created Transportation tender")
        if self.is_closed:
            btn_click("announce_tender_closed")
        if self.has_price_list and self.is_transportation == False:
            self.create_price_list_announcer()
            if self.has_custom_fields == True:
                self.create_custom_fields_announcer()
        calendar_input("announce_tender_calendar_deadline", get_submission_deadline())
        calendar_input("announce_tender_calendar_start", datetime.now().strftime("%Y-%m-%d %H:%M"))

    def add_spot_general_info(self) -> None:
        btn_click("announce_spot_btn")
        self.create_price_list_announcer()
        if self.has_custom_fields:
            self.create_custom_fields_announcer()
        calendar_input("announce_tender_calendar_deadline", get_submission_deadline())

    def add_tender_admin(self):
        pass

    def approve_tender_admin(self, tender_id: str) -> None:
        sign_in("admin")

        pass

    def indicate_cpv_category(self):
        pass

    def create_price_list_announcer(self) -> None:
        """Creates price list in announcer - General info page"""
        try:
            btn_click("announce_tender_price_list_btn")
            myvar = find("announce_tender_price_list_name_input")
            try:
                myvar.send_keys("test")
            except Exception as err:
                print_to_log(f"Error with create_price_list_announcer. Couldn't use send_keys {err}")
            time.sleep(1)
            myvar = find("announce_tender_price_list_name_input")
            btn_click("announce_tender_price_list_name_input")
            myvar.clear()
            box_type("announce_tender_price_list_name_input", "test")
            box_type("announce_tender_price_list_amount", "5.00")
            select_unit("announce_tender_price_list_unit_list", 1)
            btn_click("announce_tender_price_list_add_product")
            btn_click("announce_tender_price_list_close_btn")
        except Exception as err:
            print_to_log(f"Error with create_price_list_announcer func. Error: {err}")

    def create_custom_fields_announcer(self):
        try:
            if self.is_spot:
                btn_click("announce_tender_custom_fields_btn_spot")
            else:
                btn_click("announce_tender_custom_fields_btn")
            btn_click("announce_tender_custom_fields_template_btn")
            btn_click("announce_tender_custom_fields_main_template")
            btn_click("announce_tender_custom_fields_close_btn")
        except Exception as err:
            print_to_log(f"Error with create_custom_fields_announcer func. Error: {err}")

    def invite_companies(self):
        participant = env_accounts["participant1"]
        box_type("announce_tender_invitations_company_input", participant["company_name"])
        box_type("announce_tender_invitations_mail_input", participant["mail"])
        if self.is_spot is False:
            box_type("announce_tender_invitations_id_input", participant["ID"])
        btn_click("announce_tender_invitations_add_btn")


    def erase_drafts(self):
        sign_in("announcer")
        btn_click("dashboard")
        for _ in range(15):
            btn_click("draft_erase_btn")
            wait.until(EC.alert_is_present())
            alert = Alert(driver)
            alert.accept()

