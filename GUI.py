import tkinter as tk
from tkinter import ttk
from functions import *

test_env = True  # To work on main, indicate test_env = False and sent to init func

default_parameters = {
    'is_spot': False,
    'is_closed': True,
    'has_price_list': False,
    'has_custom_fields': False,
    'has_invitations': False,
    'is_transportation': False,
    'tender_id': None,
    'spot_link': None,
    'tender_name': None,
    'test_env': True,
}


class TenderGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tender Management System")
        self.style = ttk.Style()
        self.style.configure('TestEnv.TCheckbutton', background='#cfe2f3', font=('Times', '16', 'bold'))

        # Tender Type
        self.tender_type_var = tk.StringVar()
        ttk.Label(self.window, text="Tender Type:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Radiobutton(self.window, text="SPOT", variable=self.tender_type_var, value="SPOT",
                        command=self.update_ui).grid(row=0, column=1)
        ttk.Radiobutton(self.window, text="Tender", variable=self.tender_type_var, value="Tender",
                        command=self.update_ui).grid(row=0, column=2)
        ttk.Radiobutton(self.window, text="Transport", variable=self.tender_type_var, value="Transport",
                        command=self.update_ui).grid(row=0, column=3)

        # Test Env
        self.test_env_var = tk.BooleanVar()
        ttk.Checkbutton(self.window, text="Production", variable=self.test_env_var, style='TestEnv.TCheckbutton',
                        command=self.update_ui).grid(row=0, column=5, padx=10, pady=(5, 0))

        # Checklist
        self.price_list_var = tk.BooleanVar()
        self.custom_fields_var = tk.BooleanVar()
        self.invitations_var = tk.BooleanVar()
        self.closed_var = tk.BooleanVar()

        ttk.Label(self.window, text="Checklist:").grid(row=1, column=0, padx=10, pady=5)
        self.price_list_checkbox = ttk.Checkbutton(self.window, text="Price List", variable=self.price_list_var,
                                                   command=self.update_ui)
        self.custom_fields_checkbox = ttk.Checkbutton(self.window, text="Custom Fields",
                                                      variable=self.custom_fields_var,
                                                      command=self.update_ui)
        ttk.Checkbutton(self.window, text="Invitations", variable=self.invitations_var,
                        command=self.update_ui).grid(row=1, column=3)
        self.closed_checkbox = ttk.Checkbutton(self.window, text="Closed", variable=self.closed_var,
                                               command=self.update_ui)
        self.price_list_checkbox.grid(row=1, column=1)
        self.custom_fields_checkbox.grid(row=1, column=2)
        self.closed_checkbox.grid(row=1, column=4)

        # Input Fields
        ttk.Label(self.window, text="Tender ID:").grid(row=2, column=0, padx=10, pady=5)
        self.tender_id_entry = ttk.Entry(self.window)
        self.tender_id_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.window, text="Tender Name:").grid(row=2, column=2, padx=10, pady=5)
        self.tender_name_entry = ttk.Entry(self.window)
        self.tender_name_entry.grid(row=2, column=3, pady=5)

        ttk.Label(self.window, text="SPOT Link:").grid(row=2, column=4, padx=10, pady=5)
        self.spot_link_entry = ttk.Entry(self.window, state='disabled')
        self.spot_link_entry.grid(row=2, column=5, pady=5, padx=(0, 10))

        # Buttons
        ttk.Button(self.window, text="Create", command=self.create_tender).grid(row=3, column=0, pady=10)
        ttk.Button(self.window, text="Participate", command=self.participate_tender).grid(row=3, column=1, pady=10)
        ttk.Button(self.window, text="Manage", command=self.manage_tender).grid(row=3, column=2, pady=10)
        ttk.Button(self.window, text="Clear", command=self.clear_fields).grid(row=3, column=3, pady=10)
        ttk.Button(self.window, text="Clarifications", command=self.clear_fields).grid(row=4, column=0, pady=10)
        ttk.Button(self.window, text="Notifications", command=self.clear_fields).grid(row=4, column=1, pady=10)
        ttk.Button(self.window, text="Erase", command=self.clear_fields).grid(row=4, column=2, pady=10)





        # Participant Dropdown

        self.participant_var = tk.StringVar(value="participant1")  # Set the default value to "participant1"
        participants = ["participant1", "participant2"]  # Add your participant choices here

        participant_menu = tk.OptionMenu(self.window, self.participant_var, *participants)
        participant_menu.grid(row=3, column=5, pady=5, padx=(0, 10))

        # Initialize UI based on default values
        self.update_ui()

    def update_ui(self):
        """Disable/Enable objects according to indicated attributes"""
        if self.tender_type_var.get() == "SPOT":
            self.spot_link_entry.config(state='normal')
            self.closed_checkbox.config(state='disabled')
            self.price_list_checkbox.config(state='disabled')
            self.custom_fields_checkbox.config(state='normal')

            self.price_list_var.set(True)
            self.closed_var.set(True)

        elif self.tender_type_var.get() == "Transport":
            self.spot_link_entry.config(state='disabled')
            self.closed_checkbox.config(state='normal')
            self.price_list_checkbox.config(state='disabled')
            self.custom_fields_checkbox.config(state='disabled')

            self.price_list_var.set(False)
            self.custom_fields_var.set(False)

        else:
            self.spot_link_entry.config(state='disabled')
            self.closed_checkbox.config(state='normal')

            self.price_list_checkbox.config(state='normal')
            self.custom_fields_checkbox.config(state='normal')

        if self.price_list_var.get() == False:
            self.custom_fields_checkbox.config(state='disabled')

        # Disable/Enable Price List and Custom Fields based on Transport

    def clear_fields(self):
        # Clear all input fields and checkboxes
        self.tender_type_var.set("")
        self.price_list_var.set(False)
        self.custom_fields_var.set(False)
        self.invitations_var.set(False)
        self.closed_var.set(False)
        self.tender_id_entry.delete(0, tk.END)
        self.spot_link_entry.delete(0, tk.END)
        self.tender_name_entry.delete(0, tk.END)

    def get_params_from_gui(gui_instance):
        tender_parameters = default_parameters

        global test_env
        # Retrieve values from the GUI instance
        tender_type = gui_instance.tender_type_var.get()
        price_list = gui_instance.price_list_var.get()
        custom_fields = gui_instance.custom_fields_var.get()
        invitations = gui_instance.invitations_var.get()
        closed = gui_instance.closed_var.get()
        tender_id = gui_instance.tender_id_entry.get()
        spot_link = gui_instance.spot_link_entry.get()
        tender_name = gui_instance.tender_name_entry.get()
        test_env = gui_instance.test_env_var.get()

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

        return tender_parameters

    def create_tender(self):
        # Implement your create tender logic here
        print("Create Tender")
        driver = init("tenders.ge", test_env)
        tender = Tender(**self.get_params_from_gui())
        tender.add_procurement()

    def participate_tender(self):
        # Implement your participate tender logic here
        print("Participate Tender")
        driver = init("tenders.ge", test_env)
        tender = Tender(**self.get_params_from_gui())
        participant_choice = self.participant_var.get()
        print(participant_choice)
        tender.upload_offer(participant_choice)

    def manage_tender(self):
        # Implement your manage tender logic here
        print("Manage Tender")
        tender = Tender(**self.get_params_from_gui())
        # Add the newly made function here

    @staticmethod
    def erase_drafts(self):
        print("Erase Drafts")
        driver = init("tenders.ge", test_env)
        Tender.erase_drafts()


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = TenderGUI()
    gui.run()
