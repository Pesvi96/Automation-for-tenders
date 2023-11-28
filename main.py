from functions import *
from datetime import date



with open("Logs/logs.txt", mode="w", encoding='utf-8') as file:
    file.write(f"Let's go.\n\nDate: {date.today().strftime("%B %d, %Y")}\n\n\n")

driver = init("http://dev2.tenders.ge")









# driver.quit()

#TODO: Cannot find description input element. Also need to add calendar input element