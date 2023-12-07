from functions import *
from datetime import date

with open("Logs/logs.txt", mode="w", encoding='utf-8') as file:
    file.write(f"Let's go.\n\nDate: {date.today().strftime("%B %d, %Y")}\n\n\n")

# dev2 _ http://dev2.
# main _ https://

test_env = True  # To work on main, indicate test_env = False and sent to init func

driver = init("tenders.ge/", test_env)

# Add E-Tender

e_tender = Tender(has_price_list=True, has_custom_fields=True, is_spot=False, has_invitations=True)
# e_tender_ID = e_tender.add_tender()
# e_tender.erase_drafts()
e_tender.approve_tender_admin("1035")



# driver.quit()

#TODO 1: Admin Approval
#TODO 2: Indicated CPV category func

