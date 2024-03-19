# Automation-for-Tenders
Test automation for Tenders.ge website

For review purposes only. Script cannot be executed, as the database for all the links and account info has been removed for security purposes.

Tender types explanation
---------------------------
Can be either E-Tender, Transportation tender or SPOT Tender
attributes:
- Can be open or closed (is_closed)
- Can have a price list (has_price_list)
- If Price list is present, can have Custom Fields (has_custom_fields)
- Can have invitations (has_invitations)


Current functionality
---------------------------
- Sign in
- Sign out
- Create Tender
- Participate in Tender
- Manage Tender results
- Create Tender attributes database
- Find Tenders in database according to Tender ID

For every action Tender class object is created with all the descriptors. The data of particular tender is saved in tender_parameters json (separate for test and production environment).


### ROADMAP

- Develop Selenium web test automation
  - Sign in
  - Sign out
  - Add Tender func (Closed/Open, Standard/Price List+Custom Fields/Transportation)
  - Publish Tender (with received variable name)
  - Add SPOT
  - Participate in Procurement (with received variable name and options - if transportation, elif price list+custom fields + standard procedures)
  - Participate in SPOT
  - Announcer actions (with received variable name)
  - Database
  - Test Suites
- Integrate the developed script into PyTest
