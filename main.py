from functions import *

with open("Logs/logs.txt", mode="w", encoding='utf-8') as file:
    file.write(f"Let's go.\n\nDate: {date.today().strftime("%B %d, %Y")}\n\n\n")

app_on = True
env
# dev2 _ http://dev2.
# main _ https://

test_env = True  # To work on main, indicate test_env = False and sent to init func
driver = init("tenders.ge", test_env)

# Add E-Tender

# e_tender = Tender(is_closed=True, is_transportation=False, has_price_list=False, has_custom_fields=False, is_spot=False,
#                   has_invitations=True, tender_id="1187")
# # e_tender.add_procurement()
# # e_tender.upload_offer()
# e_tender.declare_result()
# # e_tender.erase_drafts()

# driver.quit()


# TODO 1: Clarifications and Notifications
# TODO 2: Cancel tender, reject tender, announce winner and evaluate, Failed?
# TODO 3: Add envelope to the parameters
# TODO 4: Add terminal status to the parameters
# TODO 5: Add Failed status?
# TODO 6: Check get_submission_deadline function, something wrong with time, particularly when it's xx:55


# TODO: Check all function docstrings

while app_on:
    env = input(
        "\n\n\n\t***\nHello. This is Testing app for Tenders.ge. Please indicate, "
        "are you on production environment? Type y/n\n")
    if env == 'y':
        test_env = False
    action_type = input("Please indicate what action would you like to perform.\n"
                        "1. Create procurement\n2. Participate\n3. Manage result page\n4. Erase drafts\n5. Exit\n")
    if action_type == '5':
        app_on = False
    elif action_type == "4":
        Tender.erase_drafts()
    else:
        tender = Tender(**receive_params())
        if action_type == "1":
            print("\t----Starting procurement creation process\n\n\n")
            tender.add_procurement()
        elif action_type == "2":
            # Participate in tender here
            answer = input("So you want to participate. Is it going to be SPOT by any chance?\n")
            if answer == 'y':
                answer = input("Then I will need the SPOT link please. Please mind the environment you are in\n")
                tender.spot_link = answer
            answer = input("Which user would you like to use, participant1 or participant2? ")
            print("\n\n\t----Uploading offer\n\n\n")
            tender.upload_offer(answer)
        elif action_type == "3":
            # Manage results here
            answer = input("So you have decided to declare a result. Please indicate which "
                           "status you would like to achieve:\n"
                           "1. Winner\n2. Awarded\n3. Canceled\n4. Rejected\n")
            tender.declare_result(answer)
