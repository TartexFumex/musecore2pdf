from selenium import webdriver
from selenium.webdriver.common.by import By

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfMerger

import requests
import time
import tempfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configparser import ConfigParser

config = ConfigParser()
config.read("config.conf")

url = config.get("general", "url")
render_path = config.get("general", "render_path")
file_name = config.get("general", "file_name")

# open the browser
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)
print("[INFO] Browser opened")
browser.get(url)
print("[INFO] Page loaded")

# remove the cookie banner
try:
    print("[INFO] Removing cookie banner")
    browser.find_element(By.CLASS_NAME, "css-1ucyjdz").click()
except:
    pass

# get the number of pages
scroll_widget = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "jmuse-scroller-component")))
pages = browser.find_elements(By.CLASS_NAME, "EEnGW")
nb_pages = len(pages)

# get the temporary dir to save the svg files
temp_dir = tempfile.mkdtemp()
print(f"Temporary directory: {temp_dir}")

browser.execute_script(f"arguments[0].scrollTop += {15};", scroll_widget)
for i in range(nb_pages):
    print(f"[INFO] Rendering page {i+1}/{nb_pages}")
    # wait for the image to load
    img = None
    while img == None:
        time.sleep(0.5)
        img = pages[i].find_element(By.TAG_NAME, "img").get_attribute("src")

    if ".svg" in img:
        r = requests.get(img)
        open(fr"{temp_dir}\page{i}.svg","w", encoding='utf-8').write(r.text)

        # Convert the svg file to pdf
        print(img)
        drawing = svg2rlg(fr"{temp_dir}\page{i}.svg")
        renderPDF.drawToFile(drawing,fr"{temp_dir}\page{i}.pdf")

    elif ".png" in img:
        print("[WARNING] PNG image detected, the quality may be reduced")

        r = requests.get(img)
        open(fr"{temp_dir}\page{i}.png","wb").write(r.content)

        c = canvas.Canvas(fr"{temp_dir}\page{i}.pdf", pagesize=A4)
        img_ = ImageReader(fr"{temp_dir}\page{i}.png")
        c.drawImage(img_, 0, 0, A4[0], A4[1])
        c.save()

    else:
        print(f"[ERROR] Unknown image format: {img}")

    # get the height of the page
    taille = pages[i].get_attribute("style")
    taille = taille.replace("width: ", "")
    taille = taille.replace("height: ", "")
    taille = taille.replace("px;", "")
    taille = taille.split(" ")
    height = int(taille[0])
    height = int(float(taille[1]))
    

    # scroll down to load the next page
    browser.execute_script(f"arguments[0].scrollTop += {height+15};", scroll_widget)
    time.sleep(0.5)
    browser.execute_script(f"arguments[0].scrollTop += {-20};", scroll_widget)
    time.sleep(0.5) 
    browser.execute_script(f"arguments[0].scrollTop += {20};", scroll_widget)

browser.close()

# merge the pdf files
merger = PdfMerger()

for i in range(nb_pages):
    merger.append(fr"{temp_dir}\page{i}.pdf")

if ".pdf" not in file_name:
    file_name += ".pdf"

print(f"[INFO] Saving the file to {render_path}\{file_name}")
merger.write(fr"{render_path}\{file_name}")
merger.close()     
print(f"[INFO] You can now access your file : {render_path}\{file_name}")