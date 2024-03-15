from datetime import datetime, date
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
    ElementClickInterceptedException, StaleElementReferenceException
import traceback
import time
import re

driver: WebDriver
env_accounts: dict
wait: WebDriverWait
env: str
action: ActionChains
MAX_TRIES = 3

default_parameters = {
    'is_spot': False,
    'is_closed': True,
    'has_price_list': False,
    'has_custom_fields': False,
    'has_invitations': False,
    'is_transportation': False,
    'tender_id': str,
    'spot_link': str,
    'tender_name': str,
}


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
    driver.implicitly_wait(10)
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


def find(element_name: str, is_plural=False, in_element: WebElement = None) -> WebElement | list[WebElement] | None:
    """Receives string for element_name. Can be used to look for list of elements or just an element.
    Finds the element parameters in elements dictionary and returns WebElement object/list, returns None if not found.
    Can be used to search inside element (e.g. div)"""
    element_type, element_value = links[element_name]
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((element_type, element_value)))
        if in_element is None:
            if is_plural:
                element = driver.find_elements(by=element_type, value=element_value)
            else:
                element = driver.find_element(by=element_type, value=element_value)
        else:
            if is_plural:
                element = in_element.find_elements(by=element_type, value=element_value)
            else:
                element = in_element.find_element(by=element_type, value=element_value)


    except NoSuchElementException:
        print_to_log(f"Element {element_name} does not exist. Current URL: {driver.current_url}.")
        return None
    except Exception as err:
        print_to_log(
            f"Error with find func. Looking for: {element_name}. Current URL: {driver.current_url}. Error: {err}."
            f"\nTraceback: {traceback.format_exc()}")
        return None
    else:
        return element


def btn_js_click(element_name):
    element = find(element_name)
    driver.execute_script("arguments[0].click();", element)


def btn_click(element_name: str, in_element=None) -> None:
    """Clicks the indicated element. Receives name of the element from links dictionary. Has find function inside it.
    Can receive in_element webelement. If element is tale, will try clicking again in a second once
     Error check provided. Doesn't return anything"""
    try:
        btn = find(element_name=element_name, in_element=in_element)
        btn.click()
    except ElementClickInterceptedException:
        print_to_log(f"Element {element_name} not clickable. Current URL: {driver.current_url}")
        raise
    except StaleElementReferenceException:
        time.sleep(1)
        btn.click()
    except Exception as err:
        print_to_log(
            f"Error with btn_click func. Element_name {element_name}. Current URL: {driver.current_url}. Error: {err}")
        raise


def get_element_value(element_name: str) -> str:
    element = find(element_name)
    if element.get_attribute('value') is not None:
        element_value = element.get_attribute('value')
        print_to_log("get_element_value func. Tried value for check")
    elif element.get_attribute('textContent') is not None:
        element_value = element.get_attribute('textContent')
        print_to_log("get_element_value func. Tried textContent for check")
    else:
        element_value = element.text
        print_to_log("get_element_value func. Tried .text for check")
    return element_value


def box_type(element_name: str, value: str, addition: str = None) -> None:
    """Types the value in the indicated element. Checks if the value in
    the element is right after typing. If a symbol is added to input after typing,
    you can indicate it in addition var. Error check provided"""
    try:
        element = find(element_name)
        element_value = get_element_value(element_name)
        if addition is not None:
            print_to_log("box_type func: It's an addition, adding value to addition")
            value = element_value + addition
        element.send_keys(value)
        element_value = get_element_value(element_name)

        if element_value != value:
            for x in range(3):
                print_to_log(
                    f"\t* Little hiccup in box_type func. Value received: {value} type {(type(value))},"
                    f" value of input field:{element_value}, type {type(element_value)}\n\tTrying again...\n")
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


# TODO: MCE gets stuck from time to time. Needs check
def mce_type(element_name: str, value: str) -> None:
    """Types the value in the indicated TinyMCE element. Checks if the value in
    the element is right after typing. Error check provided"""
    try:
        mce = find(element_name)
        driver.switch_to.frame(mce)
        box_type("announce_tender_description_input_body", value)
        # element_value = get_element_value(element_name)
        # if element_value != value:
        #     for x in range(3):
        #         print_to_log("mce_type func: element value was not equal to designated value. Trying box_type again")
        #         box_type("announce_tender_description_input_body", value)
        #         element_value = get_element_value(element_name)
        #         if element_value == value:
        #             break
        #         if x == 2:
        #             raise Exception("Tried mce_type func 3 times, didn't work")
        driver.switch_to.default_content()
    except Exception as err:
        print_to_log(f"Error with mce_Type func. Error: {err}")
    else:
        print_to_log("MCE Typed successfully")


def get_submission_deadline() -> str:
    """Returns present time+5 minutes"""
    now_plus_5_minutes = datetime.now()
    if now_plus_5_minutes.minute > 55:
        now_plus_5_minutes = now_plus_5_minutes.replace(hour=now_plus_5_minutes.hour + 1, minute=5 - (60 - now_plus_5_minutes.minute))
    else:
        now_plus_5_minutes = now_plus_5_minutes.replace(minute=now_plus_5_minutes.minute + 5)
    return now_plus_5_minutes.strftime("%Y-%m-%d %H:%M")


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
    except Exception:
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
        driver.get(env + "tenders.ge")
        an_reg_btn = find("announce/register_btn")
        if an_reg_btn.text == "გამოცხადება":
            print_to_log("Already signed in. Signing out")
            sign_out()
        btn_click("sign_in_btn")
        box_type("sign_in_mail", env_accounts[user]["mail"])
        print(f"\n\n\t\t{env_accounts[user]["pass"]}\n\n\n{env_accounts[user]["mail"]}")
        box_type("sign_in_pass", env_accounts[user]["pass"])
        btn_click("sign_in_submit_btn")
        if user != "admin":
            driver.get(f"{env}tenders.ge/profile/company-info")
            company_name = find("profile_company_name").text  # Does it check the sign in? There's no raise
            if company_name != env_accounts[user]["company_name"]:
                print_to_log(f"The user signed in is not right. User displayed: {company_name}. Trying again")
                sign_in(user)
    except Exception as err:
        print_to_log(f"Error with sign_in func. Error: {err}")
        return False
    else:
        print_to_log(f"Signed in successfully to {env_accounts[user]["company_name"]}")
        return True


def sign_out() -> None:
    """Signs out from present account. Doesn't return anything """
    try:
        btn_click("company_dropdown_list")
        btn_click("sign_out_btn")
    except Exception as err:
        print_to_log(f"Error with sign_out func. Error: {err}")
    else:
        print_to_log("Signed out successfully")


# def receive_params() -> dict:
#     tender_parameters = default_parameters
#     answer = input("Okay now let's figure out the parameters. Let's go one by one. Is it SPOT? type y/n\n")
#     if answer == "y":
#         print("So it is SPOT you seek")
#         tender_parameters["is_spot"] = True
#         tender_parameters["has_price_list"] = True
#         tender_parameters["has_invitations"] = True
#         answer = input("Would this SPOT one have custom fields?")
#         if answer == 'y':
#             tender_parameters["has_custom_fields"] = True
#     else:
#         tender_parameters["is_spot"] = False
#         print("So it is a mere E-Tender you seek")
#         answer = input("Is it a transportation tender, padawan?\n")
#         if answer == 'y':
#             print("Transportation it is")
#             tender_parameters["is_transportation"] = True
#         else:
#             tender_parameters["is_transportation"] = False
#             print("A standard E-Tender you shall find\n")
#             answer = input("Shall it provide is with a price list, my young one?\n")
#             if answer == 'y':
#                 tender_parameters["has_price_list"] = True
#                 answer = input("And a custom field for an individual like you?\n")
#                 if answer == 'y':
#                     tender_parameters["has_custom_fields"] = True
#             else:
#                 tender_parameters["has_price_list"] = False
#         answer = input("Is it a closed one, grasshopper?\n")
#         if answer == 'n':
#             tender_parameters["is_closed"] = False
#         else:
#             tender_parameters["is_closed"] = True
#     answer = input("Almost done. Do you seek a particular ID? if yes, type it in, if not, just type n\n")
#     if answer != 'n':
#         tender_parameters["tender_id"] = answer
#     else:
#         tender_parameters["tender_id"] = None
#     return tender_parameters


class Tender:

    def __init__(self, is_spot=False, is_closed=True, has_price_list=False, has_custom_fields=False,
                 has_invitations=False, is_transportation=False, tender_id: str = None, spot_link: str = None,
                 tender_name: str = None, test_env=True):
        """Creates an open E-Tender without Price List and has_invitations as a default"""
        self.is_spot = is_spot
        self.is_closed = is_closed
        self.has_price_list = has_price_list
        self.has_custom_fields = has_custom_fields
        self.has_invitations = has_invitations
        self.is_transportation = is_transportation
        self.tender_id = tender_id
        self.spot_link = spot_link
        self.tender_name = tender_name
        # self.test_env = test_env
        print(f"Tender class init method parameters: spot: {self.is_spot}, closed: {self.is_closed}, "
              f"price: {self.has_price_list}, custom: {self.has_custom_fields}, invites: {self.has_invitations}"
              f"transport: {self.is_transportation}, tenderid {self.tender_id}, spotlink {self.spot_link}"
              f"name: {self.tender_name}")

    def add_procurement(self) -> None:
        """
        Receives params to check which type tender you want.
        is_spot: True / False (SPOT if true, E-Tender if False, announcement not needed)
        is_closed: True / False
        has_price_list: True / False
        has_custom_fields: True / False
        has_invitations: True / False
        is_transportation: True / False
        """

        def add_etender_general_info() -> None:
            btn_click("announce_etender_btn")
            if self.is_transportation:
                btn_js_click("announce_tender_transportation_yes_btn")
                price_list_btn = find(
                    "announce_tender_price_list_btn")  # Somehow clicking transportation radio locks price list
                # button, next line is for that
                driver.execute_script("arguments[0].classList.remove('btn-disabled');", price_list_btn)
                print_to_log("Created Transportation tender")
            if self.is_closed:
                btn_click("announce_tender_closed")
            if self.has_price_list and self.is_transportation is False:
                create_price_list_announcer()
                if self.has_custom_fields is True:
                    create_custom_fields_announcer()
            calendar_input("announce_tender_calendar_deadline", get_submission_deadline())
            calendar_input("announce_tender_calendar_start", datetime.now().strftime("%Y-%m-%d %H:%M"))

        def add_spot_general_info() -> None:
            btn_click("announce_spot_btn")
            create_price_list_announcer()
            if self.has_custom_fields:
                create_custom_fields_announcer()
            calendar_input("announce_tender_calendar_deadline", get_submission_deadline())

        def create_price_list_announcer() -> None:
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

        def create_custom_fields_announcer():
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

        def invite_companies():
            participant = env_accounts["participant1"]
            box_type("announce_tender_invitations_company_input", participant["company_name"])
            box_type("announce_tender_invitations_mail_input", participant["mail"])
            if self.is_closed and not self.is_spot:
                box_type("announce_tender_invitations_id_input", participant["ID"])
            btn_click("announce_tender_invitations_add_btn")
            participant = env_accounts["participant2"]
            box_type("announce_tender_invitations_company_input", participant["company_name"])
            box_type("announce_tender_invitations_mail_input", participant["mail"])
            if self.is_closed and not self.is_spot:
                box_type("announce_tender_invitations_id_input", participant["ID"])
            btn_click("announce_tender_invitations_add_btn")

        sign_in("announcer")
        btn_click("announce/register_btn")
        if self.is_spot:
            add_spot_general_info()
        else:
            add_etender_general_info()
        if self.tender_name == '':
            box_type("announce_tender_title_input", "Automation Tender")
        else:
            box_type("announce_tender_title_input", self.tender_name)
        time.sleep(2)
        box_type("announce_tender_email_input", env_accounts["announcer"]["mail"])
        mce_type("announce_tender_description_input", "test")
        btn_click("add_tender_btn_class")
        if self.is_spot is False:  # If it's a tender, indicate CPV category
            btn_click("announce_tender_category_checkbox")
            btn_click("add_tender_btn_class")
        btn_click("add_tender_btn_class")  # Click next on Documentation page
        if self.has_invitations:
            invite_companies()
        print_to_log("Looking for next button in invitations page")
        btn_click("add_tender_btn_class")
        tender_full_name = find("announce_tender_preview_title").get_attribute('textContent')
        self.tender_id = (re.findall('[S|T]([0-9]+)', tender_full_name))[0]  # Returns tender id as a string
        print_to_log(f"Tender ID: {self.tender_id}")
        if self.is_spot:
            btn_click("announce_tender_spot_preview_submit_btn")
        else:
            driver.get(env + "tenders.ge/action/send-for-approval/" + self.tender_id)
            self.approve_tender_admin()
        return self.tender_id

    def approve_tender_admin(self) -> None:
        sign_in("admin")
        print(self.tender_id)
        driver.get(env + "tenders.ge/admin/tender-manager/preview/" + self.tender_id)
        btn_click("admin_panel_publish_tender_btn")

    def upload_offer(self, participant):
        """Goes to the offer page and uploads document + offer. Signs into participant acc if needed"""

        def upload_offer_doc():
            try:
                btn_click("offer_document_upload_btn")
                file_input = find("offer_document_upload_btn_2")
                file_path = "C:/Users/user/PycharmProjects/Automatisation-for-Tenders/Logs/logs.txt"
                file_input.send_keys(file_path)
                btn_click("offer_document_upload_submit")
            except Exception as err:
                print_to_log(f"Error with upload_offer_doc func. Error: {err} ")

        def upload_offer_price_list():
            """Uploads Price list"""
            try:
                btn_click("offer_price_list_btn")
                box_type("offer_price_list_analog", "test")
                offer_price_list_price = find("offer_price_list_price")
                offer_price_list_price.send_keys("5")
                btn_click("offer_price_list_submit")
            except Exception as err:
                print_to_log(f"Error with upload_offer_price_list func. Error: {err}")

        def upload_offer_custom_fields():
            """Fills custom fields according to main template. Error check provided"""
            try:
                btn_click("offer_custom_fields_yes/no")
                select_unit("offer_custom_fields_multiple_choice", 2)
                box_type("offer_custom_fields_short_text", "short text")
                box_type("offer_custom_fields_long_text", "long text")
                box_type("offer_custom_fields_numbers", "123")
                percent = find("offer_custom_fields_percent")
                percent.send_keys("15")
                calendar_input("offer_custom_fields_calendar", datetime.now().strftime("%Y-%m-%d %H:%M"))
            except Exception as err:
                print_to_log(f"Error with upload_offer_custom_fields func. Error: {err}")

        def upload_offer_standard_price():
            try:
                box_type("offer_standard_price", "500")
                btn_click("offer_standard_price_submit")
                btn_click("offer_standard_price_submit_accept")
            except Exception as err:
                print_to_log(f"Error with upload_offer_standard_price func. Error: {err}")

        def upload_offer_transportation():
            try:
                btn_click("offer_transportation_btn")
                input_price = find("offer_transportation_input_price")
                input_price.send_keys("30")
                box_type("offer_transportation_input_transit", '15')
                select_unit("offer_transportation_select_terms", 1)
                input_days = find("offer_transportation_input_days")
                input_days.send_keys("15")
                btn_click("offer_transportation_submit")
                btn_click("offer_transport&price_list_accept_submit")
            except Exception as err:
                print_to_log(f"Error with upload_offer_transportation func. Error: {err}")

        if self.is_spot:
            driver.get(self.spot_link)
        else:
            driver.get(env + "tenders.ge")
            sign_in(participant)
            driver.get(env + "tenders.ge/tenders/proposal/" + self.tender_id)
        if find("offer_document_upload_btn") is not None:
            upload_offer_doc()
            # TODO: It can't see the doc upload button in SPOT proposal page
        if self.is_transportation:
            upload_offer_transportation()
        else:
            if self.has_price_list:
                upload_offer_price_list()
                if self.has_custom_fields:
                    upload_offer_custom_fields()
                btn_click("offer_transport&price_list_accept_submit")
            else:
                upload_offer_standard_price()

    def clarifications_question(self):
        """
        - Go to questions page
        - Type question in the question input box
        - Press send button
        - Return to various page
        """
        pass

    def clarifications_answer(self):
        """
        - Go to questions page
        - Type question in the question input box
        - Press send button
        - Return to various page
        """

    def notifications_question(self):
        pass

    def notifications_answer(self):
        pass

    def declare_result(self, status=None):
        """
        statuses:
        Current : status-info bg-primary
        Evaluation : status-info bg-blue
        Failed : status-info bg-danger
        Winner : status-info bg-purple
        Awarded : status-info bg-green
        Rejected : status-info bg-danger
        Canceled : status-info bg-danger
        """

        def result_change_status_to_winner():
            btn_click("result_action_btn")
            btn_js_click("result_action_win_btn")
            btn_js_click("result_action_confirmation_btn")

        def result_return_status_to_evaluation():
            btn_click("result_action_btn")
            btn_js_click("result_action_win_btn")
            btn_js_click("result_action_confirmation_btn")

        def result_change_status_to_awarded():
            btn_click("result_action_btn")
            btn_js_click("result_action_award_btn")
            btn_js_click("result_action_confirmation_btn")

        def result_change_status_to_rejected():
            button_class = find("result_action_btn_frame", is_plural=True)
            for x in range(len(button_class)):
                btn_click("result_action_btn", in_element=button_class[x - 1])
                btn_click("result_action_reject_btn", in_element=button_class[x - 1])
                button_class = find("result_action_btn_frame", is_plural=True)
                time.sleep(1)
            btn_js_click("result_action_confirmation_btn")

        def result_change_status_to_canceled():
            btn_click("result_action_cancellation_btn")
            btn_js_click("result_action_confirmation_btn")

        sign_in("announcer")
        driver.get(env + "tenders.ge/tenders/result/" + self.tender_id)

        if status == "Winner":
            result_change_status_to_winner()
        elif status == "Awarded":
            result_change_status_to_awarded()
        elif status == "Rejected":
            result_change_status_to_rejected()
        elif status == "Canceled":
            result_change_status_to_canceled()
        elif status == "Cancel Award":
            result_change_status_to_awarded()

        # Check if the status was changed right. Try again if not
        if self.result_get_status() != status:
            print_to_log(f"Error with declare_result func. Couldn't change status to {status}, trying again")

    def result_get_status(self):
        result_status = find("result_status_div_class")
        status_name = result_status.text
        return status_name

    @staticmethod
    def erase_drafts():
        sign_in("announcer")
        btn_click("dashboard")
        buttons = find("draft_erase_btn", is_plural=True)
        for x in range(len(buttons)):
            btn_click("draft_erase_btn")
            wait.until(EC.alert_is_present())
            alert = Alert(driver)
            alert.accept()
