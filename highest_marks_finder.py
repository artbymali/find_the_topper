from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def get_result_page(dept, year, semester, batch, subject):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://exam.usindh.edu.pk/v2/course.php") 
    
    prog = f"BS ({dept})"

    if dept in ["ENVIRONMENTAL SCIENCE", "ENVIRONMENTAL SCIENCES"]:
      dept = "CENTRE FOR ENVIRONMENTAL SCIENCES"
      prog = "BS (ENVIRONMENTAL SCIENCES)"

       
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
    (By.XPATH, f"//select[@id='dept_id']/option[text()='{dept}']")
    ))
    department = Select(driver.find_element(By.ID, "dept_id"))
    department.select_by_visible_text(dept)

    if dept == "MEDIA & COMMUNICATION STUDIES":
       dept = "MASS COMMUNICATION"
       prog = f"BS ({dept})"


    if '&' in dept:
       dept = dept.replace('&', "AND")
       prog = f"BS ({dept})"

    
    if dept == "BUSINESS ADMINSTRATION":
       prog = "B.B.A (HONS)"

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
    (By.XPATH, f"//select[@id='program_id']/option[text()='{prog}']")
    ))
    program = Select(driver.find_element(By.ID, "program_id"))
    program.select_by_visible_text(prog)

    y = Select(driver.find_element(By.ID, "exam_year"))
    y.select_by_visible_text(year)

    sem = Select(driver.find_element(By.ID, "semesterCombo"))
    sem.select_by_visible_text(semester)

    space_batch = batch+"  "
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
    (By.XPATH, f"//select[@id='batch']/option[text()='{space_batch}']")
    ))
    dropdown = Select(driver.find_element(By.ID, "batch"))

    for option in dropdown.options:
       if option.text.strip() == batch:
        dropdown.select_by_visible_text(option.text)
        break
       
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.ID, "courseNo"), subject))
    course = Select(driver.find_element(By.ID, "courseNo"))
    course.select_by_visible_text(subject)

    display_button = driver.find_element(By.ID, "display")
    display_button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "course")))
    
    html = driver.page_source
    return html

def find_topper(dept, year, semester, batch, subject):

   soup = BeautifulSoup(get_result_page(dept, year, semester, batch, subject), "html.parser")
   data = {}

   div = soup.find(class_="col-md-12")
   table = div.find("table")
   body = table.find("tbody")
   rows = body.find_all("tr")

   for row in rows:
      headers = row.find_all("th")
      if len(headers) < 6:
       continue
      
      roll_no = headers[1].text + '-'
      name = headers[2].text
      data[roll_no+name] = headers[5].text

   marks = list(data.values())
   marks.sort()
   val = marks[len(marks)-1]

   highest = [k for k, v in data.items() if v == val]
   print(f"Highest marks in {subject}: ")

   for name in highest:
      print(name + " = " + data[name])
   
   return highest
   