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

    if dept == "PHARMACY":
       prog = "DOCTOR OF PHARMACY (PHARM. D)"

    if dept == "SINDH DEVELOPMENT STUDIES CENTRE":
       prog = "BS (RURAL DEVELOPMENT)"

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
    time.sleep(1)
    html = driver.page_source
    return html

def find_topper(dept, year, semester, batch, subject):

   html = get_result_page(dept, year, semester, batch, subject)

   soup = BeautifulSoup(html, "html.parser")
   data = {}
   
   table = soup.select_one("table.table.table-bordered.table-striped")
   body = table.find("tbody")
   rows = body.find_all("tr")

   for row in rows:
      headers = row.find_all("th")
      if len(headers) < 6:
       continue
      
      roll_no = headers[1].text + ' - '
      name = headers[2].text
      data[roll_no+name] = headers[5].text

   marks = set(data.values())
   marks = list(marks)
   marks.sort()
   vals = [marks[len(marks)-1], marks[len(marks)-2], marks[len(marks)-3]]

   first = [k for k, v in data.items() if v == vals[0]]
   second = [k for k, v in data.items() if v == vals[1]]
   third = [k for k, v in data.items() if v == vals[2]]

   print(f"Highest marks in {subject}: ")

   print("FIRST: ")
   for name in first:
      print(name + " = " + data[name])

      print("SECOND: ")
   for name in second:
      print(name + " = " + data[name])
   
   print("THIRD: ")
   for name in third:
      print(name + " = " + data[name])

   return [first, second, third], [vals[0], vals[1], vals[2]] 
   