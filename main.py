from selenium import webdriver
from functions import *



driver = init("http://dev2.tenders.ge")

max_tries(sign_in, "dev2announcer")

