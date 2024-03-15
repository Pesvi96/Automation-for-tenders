import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from functions import *
import json

# To work on main, indicate test_env = False and sent to init func

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

json_filepath: str


class TenderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tender Management System")
        self.style = ttk.Style()
        self.style.configure('TestEnv.TCheckbutton', background='#cfe2f3', font=('Times', '16', 'bold'))

        # Action Dropdown
        self.action_var = tk.StringVar(value="Create")  # Set the default value to "Create"
        actions = ["Create", "Participate", "Manage", "Clarifications - Question", "Clarifications - Answer",
                   "Notifications - Question", "Notifications - Answer", "Erase"]

        tk.Label(self.window, text="Action:").grid(row=0, column=0, padx=10, pady=5)

        action_dropdown = tk.OptionMenu(self.window, self.action_var, *actions, command=lambda _: self.update_ui())
        action_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Tender Type radio
        self.tender_type_var = tk.StringVar()
        ttk.Label(self.window, text="Tender Type:").grid(row=1, column=0, padx=10, pady=5)
        self.spot_radio = ttk.Radiobutton(self.window, text="SPOT", variable=self.tender_type_var, value="SPOT",
                                          command=self.update_ui)
        self.tender_radio = ttk.Radiobutton(self.window, text="Tender", variable=self.tender_type_var, value="Tender",
                                            command=self.update_ui)
        self.transport_radio = ttk.Radiobutton(self.window, text="Transport", variable=self.tender_type_var,
                                               value="Transport",
                                               command=self.update_ui)
        self.spot_radio.grid(row=1, column=1)
        self.tender_radio.grid(row=1, column=2)
        self.transport_radio.grid(row=1, column=3)

        # Test Env
        self.is_production = tk.BooleanVar()
        ttk.Checkbutton(self.window, text="Production", variable=self.is_production, style='TestEnv.TCheckbutton',
                        command=self.update_ui).grid(row=0, column=5, padx=10, pady=(5, 0))

        # Driver btn

        ttk.Button(self.window, text="driver", command=self.driver_init).grid(row=0, column=4, padx=5, pady=5)

        # Checklist
        self.price_list_var = tk.BooleanVar()
        self.custom_fields_var = tk.BooleanVar()
        self.invitations_var = tk.BooleanVar()
        self.closed_var = tk.BooleanVar()

        ttk.Label(self.window, text="Checklist:").grid(row=2, column=0, padx=10, pady=5)
        self.price_list_checkbox = ttk.Checkbutton(self.window, text="Price List", variable=self.price_list_var,
                                                   command=self.update_ui)
        self.custom_fields_checkbox = ttk.Checkbutton(self.window, text="Custom Fields",
                                                      variable=self.custom_fields_var,
                                                      command=self.update_ui)
        self.invitations_checkbox = ttk.Checkbutton(self.window, text="Invitations", variable=self.invitations_var,
                                                    command=self.update_ui)
        self.closed_checkbox = ttk.Checkbutton(self.window, text="Closed", variable=self.closed_var,
                                               command=self.update_ui)
        self.price_list_checkbox.grid(row=2, column=1)
        self.custom_fields_checkbox.grid(row=2, column=2)
        self.closed_checkbox.grid(row=2, column=4)
        self.invitations_checkbox.grid(row=2, column=3)

        # Input Fields
        self.tender_id_var = tk.StringVar()
        ttk.Label(self.window, text="Tender ID:").grid(row=4, column=0, padx=10, pady=5)
        self.tender_id_entry = ttk.Entry(self.window, textvariable=self.tender_id_var)
        self.tender_id_entry.grid(row=4, column=1, pady=5)

        self.tender_name_var = tk.StringVar()
        ttk.Label(self.window, text="Tender Name:").grid(row=3, column=0, padx=10, pady=5)
        self.tender_name_entry = ttk.Entry(self.window, textvariable=self.tender_name_var)
        self.tender_name_entry.grid(row=3, column=1, pady=5)

        self.spot_link_var = tk.StringVar()
        ttk.Label(self.window, text="SPOT Link:").grid(row=3, column=2, padx=10, pady=5)
        self.spot_link_entry = ttk.Entry(self.window, textvariable=self.spot_link_var)
        self.spot_link_entry.grid(row=3, column=3, pady=5, padx=(0, 10))

        # Participant Dropdown

        self.participant_var = tk.StringVar(value="participant1")  # Set the default value to "participant1"
        participants = ["participant1", "participant2"]  # Add your participant choices here

        self.participant_menu = tk.OptionMenu(self.window, self.participant_var, *participants)
        self.participant_menu.grid(row=5, column=0, pady=(5, 30), padx=5)

        # Tender Result Status Dropdown
        self.result_status_var = tk.StringVar(value="Awarded")
        statuses = ["Winner", "Awarded", "Rejected", "Canceled", "Cancel Award"]

        self.status_menu = tk.OptionMenu(self.window, self.result_status_var, *statuses)
        self.status_menu.grid(row=5, column=1, pady=(5, 30), padx=5)

        # Buttons
        ttk.Button(self.window, text="Clear", command=self.clear_fields).grid(row=10, column=0, pady=10)
        ttk.Button(self.window, text="GO", command=self.perform_action).grid(row=10, column=5, pady=10)
        ttk.Button(self.window, text="Find", command=self.set_gui_from_data).grid(row=4, column=2, pady=10)
        ttk.Button(self.window, text="Add to JSON", command=self.save_parameters_to_json).grid(row=4, column=3,
                                                                                               pady=10)
        ttk.Button(self.window, text="Add").grid(row=6, column=2, padx=(20, 0))
        ttk.Button(self.window, text="Delete").grid(row=7, column=2, padx=(20, 0))
        ttk.Button(self.window, text="Run Test Suite", command=self.run_test_suite).grid(row=8, column=2, padx=(20, 0))
        ttk.Button(self.window, text="Dialog", command=self.dialog_test).grid(row=8, column=3)

        # Listbox
        self.yScroll = tk.Scrollbar(self.window, orient=tk.VERTICAL, relief='groove')

        self.test_suites_list = tk.StringVar()
        self.test_suites_box = tk.Listbox(self.window, bd=3, listvariable=self.test_suites_list, width=50,
                                          relief="groove", yscrollcommand=self.yScroll.set)
        self.test_suites_box.grid(row=6, column=0, columnspan=2, rowspan=4, padx=(10, 0), sticky=tk.N + tk.S + tk.W)
        self.yScroll.grid(row=6, column=2, sticky=tk.N + tk.S + tk.W)
        self.yScroll.config(command=self.test_suites_box.yview)

        # Initialize UI based on default values
        self.update_ui()

    def update_ui(self):
        """Disable/Enable objects according to indicated attributes"""

        def change_all_widgets(state):
            """Enables all widgets in the UI"""
            widgets = [
                self.spot_radio, self.tender_radio, self.transport_radio,
                self.price_list_checkbox, self.custom_fields_checkbox,
                self.invitations_checkbox, self.closed_checkbox,
                self.tender_id_entry, self.tender_name_entry,
                self.spot_link_entry, self.participant_menu, self.status_menu
            ]
            for widget in widgets:
                widget.config(state=state)

        """actions = ["Create", "Participate", "Manage", "Clarifications - Question", "Clarifications - Answer",
                   "Notifications - Question", "Notifications - Answer", "Erase"]"""
        change_all_widgets('normal')
        action = self.action_var.get()

        if action == "Create":
            self.tender_id_entry.config(state='disabled')
            self.spot_link_entry.config(state='disabled')
            self.participant_menu.config(state='disabled')
            self.status_menu.config(state='disabled')
        elif action == "Participate":
            self.invitations_checkbox.config(state='disabled')
            self.closed_checkbox.config(state='disabled')
            self.status_menu.config(state='disabled')
            self.tender_name_entry.config(state='disabled')
        elif action == "Manage":
            # Disable everything apart from Tender ID and status
            change_all_widgets('disabled')
            self.tender_id_entry.config(state='normal')
            self.status_menu.config(state='normal')
        elif action == "Erase":
            change_all_widgets('disabled')
        else:
            change_all_widgets('disabled')
            self.participant_menu.config(state='normal')
            self.tender_id_entry.config(state='normal')

        if self.tender_type_var.get() == "SPOT":
            self.closed_checkbox.config(state='disabled')
            self.price_list_checkbox.config(state='disabled')

            self.price_list_var.set(True)
            self.closed_var.set(True)

        elif self.tender_type_var.get() == "Transport":
            self.spot_link_entry.config(state='disabled')
            self.price_list_checkbox.config(state='disabled')
            self.custom_fields_checkbox.config(state='disabled')

            self.price_list_var.set(False)
            self.custom_fields_var.set(False)

        else:
            self.spot_link_entry.config(state='disabled')

        if self.price_list_var.get() == False:
            self.custom_fields_checkbox.config(state='disabled')

        # Disable/Enable Price List and Custom Fields based on Transport

    def driver_init(self):
        global json_filepath
        if self.is_production.get():
            test_env = False
            json_filepath = "Logs/tender_parameters_main.json"
        else:
            json_filepath = "Logs/tender_parameters_dev2.json"
            test_env = True
        init("tenders.ge", test_env)

    def dialog_test(self):
        spotlink = tk.simpledialog.askstring(title="title", prompt='\n\t\t\tdialog\t\t\t\t\n\n')
        print(spotlink)

    def perform_action(self):
        action = self.action_var.get()
        if action == "Create":
            self.create_tender()
        elif action == "Participate":
            self.participate_tender()
        elif action == "Manage":
            self.manage_tender()
        elif action == "Clarifications - Question":
            pass
        elif action == "Clarifications - Answer":
            pass
        elif action == "Notifications - Question":
            pass
        elif action == "Notifications - Answer":
            pass
        elif action == "Erase":
            self.erase_drafts()

    def clear_fields(self):
        # Clear all input fields and checkboxes
        print("Clearing fields")
        self.tender_type_var.set("")
        self.price_list_var.set(False)
        self.custom_fields_var.set(False)
        self.invitations_var.set(False)
        self.closed_var.set(False)
        self.tender_id_var.set("")
        self.spot_link_var.set("")
        self.tender_name_var.set("")

    # -------------------------- Part for getting/saving data --------------------------

    def save_parameters_to_json(self):
        """Saves tender parameters dictionary to designated json"""
        tender_parameters = self.get_params_from_gui()
        tender_id = tender_parameters["tender_id"]
        try:
            with open(json_filepath, mode='r') as f:
                tenders_data = json.load(f)
        except FileNotFoundError as err:
            print(err)
            tenders_data = {}

        tenders_data[tender_id] = tender_parameters

        try:
            with open(json_filepath, mode='w') as f:
                param_json = json.dumps(tenders_data, indent=2, sort_keys=True)
                f.write(param_json)
        except FileNotFoundError as err:
            print(err)
        else:
            print(f"Tender ID {tender_id} not found. Added it to JSON file")

    def set_gui_from_data(self, tender_parameters=None):
        """Receives dictionary of attributes. Sets data according to it"""
        if tender_parameters is None:
            tender_parameters = self.find_tender_in_logs()
        else:
            tender_parameters = tender_parameters

        self.clear_fields()

        if tender_parameters is not None:
            print(tender_parameters)
            if tender_parameters["is_spot"]:
                self.tender_type_var.set("SPOT")
            elif tender_parameters["is_transportation"]:
                self.tender_type_var.set("Transport")
            else:
                self.tender_type_var.set("Tender")

            if tender_parameters["is_closed"]:
                self.closed_var.set(True)

            if tender_parameters["has_price_list"]:
                self.price_list_var.set(True)

            if tender_parameters["has_custom_fields"]:
                self.custom_fields_var.set(True)

            if tender_parameters["has_invitations"]:
                self.invitations_var.set(True)

            if tender_parameters["spot_link"] is not None:
                self.spot_link_var.set(tender_parameters["spot_link"])

            if tender_parameters["tender_name"] is not None:
                self.tender_name_var.set(tender_parameters["tender_name"])

            if "tender_id" in tender_parameters:  # If the dictionary has tender_id. Used for Test Suites Create
                self.tender_id_var.set(tender_parameters["tender_id"])

    def find_tender_in_logs(self) -> dict | None:
        """Looks for Tender ID in JSON data, if found returns its dictionary of attributes"""
        tender_id = self.tender_id_var.get()

        with open(json_filepath, mode='r+') as f:
            try:
                tenders_data = json.load(f)
            except json.decoder.JSONDecodeError as err:
                print(err)
                tenders_data = {}
            # Checks if ID is in tender_parameters_dev2.json file
            print(f"tenders_data is: {tenders_data}")

            if tender_id in tenders_data:
                tender_parameters = tenders_data[tender_id]
                print(f"tender_parameters is: {tender_parameters}")
                f.close()
                return tender_parameters
            else:
                print("Tender not found in logs")
                return None

    # noinspection PyTypeChecker
    def get_params_from_gui(self) -> dict:
        """Gets all parameters from GUI, returns it as a dictionary"""
        tender_parameters = default_parameters
        print("\n\t\t--------get_params_from_gui func ------")
        # Retrieve values from the GUI instance
        tender_type = self.tender_type_var.get()
        price_list = self.price_list_var.get()
        custom_fields = self.custom_fields_var.get()
        invitations = self.invitations_var.get()
        closed = self.closed_var.get()
        tender_id = self.tender_id_var.get()
        spot_link = self.spot_link_var.get()
        tender_name = self.tender_name_var.get()
        print(f"tender_type = {tender_type}\nprice_list = {price_list}\ncustom_fields = {custom_fields}"
              f"\ninvitations = {invitations}\nclosed = {closed}\ntender_id = {tender_id}\n"
              f"spot_link = {spot_link}\ntender_name = {tender_name}")

        # Update tender_parameters based on GUI values
        if tender_type == "SPOT":
            tender_parameters["is_spot"] = True
            tender_parameters["is_transportation"] = False
        elif tender_type == "Transport":
            tender_parameters["is_spot"] = False
            tender_parameters["is_transportation"] = True
        else:
            tender_parameters["is_spot"] = False
            tender_parameters["is_transportation"] = False

        tender_parameters["has_price_list"] = price_list
        tender_parameters["has_custom_fields"] = custom_fields
        tender_parameters["has_invitations"] = invitations
        tender_parameters["is_closed"] = closed
        tender_parameters["tender_id"] = tender_id
        tender_parameters["spot_link"] = spot_link
        tender_parameters["tender_name"] = tender_name
        # tender_parameters["test_env"] = test_env

        print(f"Result parameters:\n------\n{tender_parameters}\n------")
        return tender_parameters

    # ----------------------------Test Suit part --------------------------------------

    def run_test_suite(self):
        def perform_test_suite_action(action: str):
            if action == 'Create':
                self.set_gui_from_data(actions_dictionary[action])
                self.create_tender()
            elif action == "Participate":
                pass
            elif action == "Manage":
                pass

        test_suite = "first_suite"  # Here must be Listbox variable

        with open("./Logs/test_suites.json", mode='r+') as f:
            try:
                test_suites_list = json.load(f)
            except json.decoder.JSONDecodeError as err:
                print(err)
                test_suites_list = {}
            print(test_suites_list)

        if test_suite in test_suites_list:
            actions_dictionary = test_suites_list[test_suite]  # Receives test suite dictionary

        for suite_action in actions_dictionary:
            perform_test_suite_action(suite_action)

    # ---------------------------------------------------------------------------------

    def create_tender(self):
        """Create procurement action. Activates add_procurement func in functions.py"""
        print("Create Tender")
        tender_parameters = self.get_params_from_gui()
        tender = Tender(**tender_parameters)
        tender.add_procurement()
        self.tender_id_var.set(tender.tender_id)
        self.save_parameters_to_json()

    def participate_tender(self):
        # Implement your participate tender logic here
        print("Participate Tender")
        tender = Tender(**self.get_params_from_gui())
        participant_choice = self.participant_var.get()
        print(participant_choice)
        tender.upload_offer(participant_choice)

    def manage_tender(self):
        # Implement your manage tender logic here
        print("Manage Tender")
        status = self.result_status_var.get()
        tender = Tender(**self.get_params_from_gui())
        tender.declare_result(status)

    @staticmethod
    def erase_drafts():
        print("Erase Drafts")
        Tender.erase_drafts()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = TenderGUI()
    gui.run()
