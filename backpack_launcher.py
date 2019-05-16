import time
import schedule
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
from emailtotext import send_simple
from os import environ

# Take a screenshot of the webpage (for testing purposes)
def save_image(name):
    name = name + ".png"
    driver.save_screenshot("output_images/" + name)
    print("Image Saved: ", name)

# Find an element and input text
def find_input_text(ID, text):
    driver.find_element_by_id(ID).click();
    driver.find_element_by_id(ID).send_keys(text);
    time.sleep(0.25)

# Clean up string only for content of interest
def clean(string):
    new = string[(string.index(">")+1):]
    if("(S1,S2)" in new):
        new = new[:(new.index("("))]
        new = new.replace("amp;", "")
    else:
        new = new[:(new.index("<"))]
    return(new)

# Scrape page for html
def get_html():
    html = driver.page_source
    html = BeautifulSoup(html, 'html.parser')
    return(html)

def get_course():
    c = str(html.find(id=("f:inside:GradedTab:j_id_jsp_394614891_19pc8:" + str(get_update()) +":courseNameClick")))
    c = clean(c)
    return(c)

def get_assignment():
    a = str(html.find(id=("f:inside:GradedTab:j_id_jsp_394614891_19pc8:" + str(get_update()) +":j_id_jsp_1186365045_18pc9:0:assignmentLink")))
    a = clean(a)
    return(a)

def get_score():
    #score/possible = grade%
    score = str(html.find(id="f:inside:GradedTab:j_id_jsp_394614891_19pc8:" + str(get_update()) + ":j_id_jsp_1186365045_18pc9:0:j_id_jsp_1186365045_42pc9"))
    score = clean(score)
    possible = str(html.find(id="f:inside:GradedTab:j_id_jsp_394614891_19pc8:" + str(get_update()) + ":j_id_jsp_1186365045_18pc9:0:j_id_jsp_1186365045_52pc9"))
    possible = clean(possible)
    grade = round(((float(score)/float(possible))*100), 1)
    return(" " + score + "/" + possible + " = " + str(grade) + "%")

def get_update(num):
    return(num)

def check_difference(old):
    old_len = len(old.find_all("tr", class_="rich-table-row dataCellEven"))
    old_len += len(old.find_all("tr", class_="rich-table-row dataCellOdd"))
    new_len = len(get_html().find_all("tr", class_="rich-table-row dataCellEven"))
    new_len += len(get_html().find_all("tr", class_="rich-table-row dataCellOdd"))
    if(old_len != new_len):
        send_simple(phone_number)
    else:
        print(' [Pass - No Update]')
        sys.stdout.write('Loading')

# Constants (Login Information)
USERNAME = "user"
PASSWORD = environ.get('password')
DAILY="https://backpack.pinecrest.edu/SeniorApps/studentParent/academic/dailyAssignments/gradeBookGrades.faces?selectedMenuId=true"

# Establish Chrome Driver
options = webdriver.ChromeOptions()
options.add_argument("--headless") # run in the background
driver = webdriver.Chrome("mybackpack-monitor/chromedriver", options=options)

# Destination page
driver.get("https://backpack.pinecrest.edu")
print("[Site Launched]")
time.sleep(0.25) # delay for loading

# Identify username and password textbox and input data
find_input_text("form:userId", USERNAME)
find_input_text("form:userPassword", PASSWORD)

# Login and Navigate to daily assignments
driver.find_element_by_id("form:signIn").click()
time.sleep(0.25)
driver.get(DAILY)

# Get html
html = get_html()

# Monitor for changes every ten minutes
schedule.every(10).minutes.do(check_difference, html)
sys.stdout.write('Loading')

while True:
    schedule.run_pending()
    sys.stdout.write('.')
    time.sleep(1)


