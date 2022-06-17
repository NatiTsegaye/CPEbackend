import os
from flask_restful import Api
from flask import Flask, request, send_file
from Main.Routes.routes import initialize_routes
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup
import requests 
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pyautogui

# driver = None
app = Flask(__name__)
api = Api(app)
CORS(app)
# CORS(app, resources=r'/*',allow_headers=[
#     "Content-Type", "Authorization", "Access-Control-Allow-Methods"])

# CORS(app, resources=r"/*",allow_headers=[
#     "Content-Type", "Authorization", "Access-Control-Allow-Methods","Access-Control-Allow-Origin"])

# app.config['MONGODB_SETTINGS'] = {
#     'host': Config.DB
# }
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup
import requests
from io import BytesIO
import skimage
import numpy as np

initialize_routes(api)


def convertImage(img):
    datas = img.getdata()
    newData = []
  
    for items in datas:
        if items[0] == 255 and items[1] == 255 and items[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(items)
  
    img.putdata(newData)
    return img; 
  

def applyFilters(images):
    newImages = []
    for image in images:
        image  = np.asarray(image)
        # num = random.randint(0,2)
        img = skimage.filters.butterworth(image, cutoff_frequency_ratio=4.6, high_pass=False, order=2.0, channel_axis=None)
        # if num==0:
        #     img = skimage.filters.butterworth(image, cutoff_frequency_ratio=4.8, high_pass=False, order=2.0, channel_axis=None)
        # elif num ==1:
        #     img =skimage.filters.hessian(image, sigmas=range(1, 10, 2), scale_range=None, scale_step=None, alpha=0.5, beta=0.5, gamma=15, black_ridges=True, mode='reflect', cval=0)
        # else:
        #     img = skimage.filters.laplace(image, ksize=4, mask=None)
        newImages.append(Image.fromarray((img*255).astype(np.uint8)))
    
    # trial1 = np.asarray(images[0])
    # img = skimage.filters.butterworth(trial1, cutoff_frequency_ratio=4.8, high_pass=False, order=2.0, channel_axis=None)
    # t1 =  Image.fromarray((img*255).astype(np.uint8))

    # trial2 = np.asarray(images[1])
    # img2 = skimage.filters.butterworth(trial2, cutoff_frequency_ratio=4.8, high_pass=False, order=2.0, channel_axis=None)
    # t2 =  Image.fromarray((img2*255).astype(np.uint8))

    # t1.paste(t2,(0,0),mask=t2.convert("RGBA"))
    x = newImages[0]
    # t1.show()
    for i in range (1,len(newImages)):
    # x.show()
        newImages[i]=newImages[i]
        x.paste(newImages[i],(0,0),newImages[i].convert('RGBA'))
        x.save("file6.png")
    return x

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route('/pr',methods=['POST'])
@cross_origin()
def post():
    body = request.get_data()
    print(body)
    req = requests.get(body)
    soup = BeautifulSoup(req.text, 'html.parser')
    img = soup.find("img",{"id":"transitionFrom--ViewInRoom"})
    print(img['src'])
    urllib.request.urlretrieve(img['srcset'].split(" ")[0],"x.jpg")
    image = Image.open("x.jpg")
    return serve_pil_image(image)

def lauchBrowser(url):
    # global driver 
    # if driver:
    #     return 
    # prefs = {"download.default_directory" : os.getcwdb().decode("utf-8") }
    options = webdriver.ChromeOptions()
    # prefs = {
    # 'download.default_directory': 'C:\\Users\\natih\\Documents\\test\\',
    # "safebrowsing.enabled": "false"
    # }
    # options.add_experimental_option("prefs",prefs)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    return driver

@app.route('/pr/process',methods=['POST'])
@cross_origin()
def anotherPost():
    body = request.get_data()
    body = body.decode("utf-8").split(',')
    images = []
    count =0
    imagePath = "C:\\Users\\natih\\Downloads\\"
    # global driver
    
    for url in body:
        count = count+1
        driver = lauchBrowser(url)
        action = ActionChains(driver)
        driver.find_element(by=By.ID, value="transitionFrom--ViewInRoom" ).click()
        driver.implicitly_wait(4)
        canvasParent = driver.find_element(by=By.CLASS_NAME, value="openseadragon-canvas")
        canvas = canvasParent.find_elements(by=By.TAG_NAME,value="canvas")[0]
        action.context_click(canvas).perform()
        pyautogui.PAUSE = 1.2
        pyautogui.press('down')
        pyautogui.press('enter')
        pyautogui.write(str(count)+'.png', interval=0.2)
        pyautogui.press('enter')
        # pyautogui.press('y')
        # pyautogui.press('enter')
        image = Image.open(imagePath + str(count)+'.png') 
        # req = requests.get(url)
        # soup = BeautifulSoup(req.text, 'html.parser')
        # img = soup.find("img",{"id":"transitionFrom--ViewInRoom"})
        # urllib.request.urlretrieve(img['srcset'].split(" ")[0],str(count)+"x.jpg")
        # image = Image.open(str(count)+"x.jpg")
        # image = convertImage(image)-ple
        images.append(image)
    driver.close()
    # driver = None

    count =0
    x = applyFilters(images)
    for url in body:
        count = count+1
        os.remove(imagePath+ str(count)+".png")
    return serve_pil_image(x)






