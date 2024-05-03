from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import json 
from selenium.webdriver.support.ui import WebDriverWait

start_time = time.time()


chrome_path = "C:/Users/USER/Downloads/chrome-win64/chrome-win64/chrome.exe"


service = Service(service=chrome_path)


ua = UserAgent()
user_agent = ua.random


chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')


driver = webdriver.Chrome(service=service, options=chrome_options)
json_data = [] 

for page in range(400, 502): 
    url = f"https://www.autosphere.fr/recherche?market=VO&page={page}&critaire_checked[]=year&critaire_checked[]=discount&critaire_checked[]=emission_co2"

    try:

        print(f"Getting data from page {page}...")
        driver.get(url)
  
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.liste-fiches > div.span4')))

        elements = driver.find_elements(By.CSS_SELECTOR, 'div.liste-fiches > div.span4')
        
        for element in elements:
            bloc1 = element.find_element(By.CLASS_NAME, 'fiche_hover') 

            mark = bloc1.find_element(By.CLASS_NAME, 'marque').text
            model = bloc1.find_element(By.CLASS_NAME, 'modele').text
            description = bloc1.find_element(By.CLASS_NAME, 'serie.ellipsis').text

            # Car characteristics
            caract_div = WebDriverWait(element, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "caract")))

            hybrid_info = caract_div.find_element(By.XPATH, './/span[1]').text
            km_info = caract_div.find_element(By.XPATH, './/span[2]').text
            year_info = caract_div.find_element(By.XPATH, './/span[3]').text
            gearbox = caract_div.find_element(By.XPATH, './/span[4]').text
         
            # Car price 
            bloc2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "bloc_prix")))

            price = bloc2.text

            # option : 
            bloc3 = element.find_element(By.CLASS_NAME, "equipement_diff_vignette")

            # Check for GPS
            try:
                gps_element = element.find_element(By.ID, "gps")
                gps = 1
            except :
                gps = 0

            # Check for rear_cam
            try:
                rear_cam_element = element.find_element(By.ID, "cam_recul")
                rear_cam = 1
            except :
                rear_cam = 0

            # Check for rear_rad
            try:
                rear_rad_element = element.find_element(By.ID, "radar_recul")
                rear_rad = 1
            except :
                rear_rad = 0

            # Check for auto_clim
            try:
                auto_clim_element = element.find_element(By.ID, "clim_auto")
                auto_clim = 1
            except :
                auto_clim = 0

            # Check for Bluetooth
            try:
                bluetooth_element = element.find_element(By.ID, "bluetooth")
                bluetooth = 1
            except :
                bluetooth = 0

            # Check for Cruise Control
            try:
                cruise_control_element = element.find_element(By.ID, "regulateur_vitesse")
                cruise_control = 1
            except :
                cruise_control = 0

            # Check for LED lights
            try:
                led_element = element.find_element(By.ID, "feux_led")
                led = 1
            except :
                led = 0

            # Check for Isofix
            try:
                isofix_element = element.find_element(By.ID, "isofix")
                isofix = 1
            except :
                isofix = 0


            item = {"mark": mark, "model": model, "description": description,
                    "fuel": hybrid_info, "km": km_info, "year": year_info, "gearbox": gearbox,
                    "isofix": isofix, "led": led, "cruise_control": cruise_control,
                    "bluetooth": bluetooth, "auto_clim": auto_clim, "rear_cam": rear_cam,
                    "rear_rad": rear_rad,"price":price}

            json_data.append(item)

    except (WebDriverException, TimeoutException) as e:
        print("Exception occurred:", e)


df = pd.DataFrame(json_data)
df.to_csv("dataset/data6.csv", index=False)

driver.quit()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time for scraping and processing data from 4 pages: {execution_time} seconds")
