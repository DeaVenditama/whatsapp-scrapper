from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import base64
import time
from datetime import datetime


class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-data-dir=~/Library/Application Support/Google/Chrome/Default/Cookies")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        print("Opening Whatsapp Web Window")
        self.driver.get('https://web.whatsapp.com')
        print("Scan Your QR Codes and Press Enter (Press Enter if You're Already Logged In)")
        input()

    def scrapeImages(self):
        try:
            print("Scrape Images From Contact Name ")
            print("Please Input a Contact Name : ")
            contact_name = input()
            print("Search Contact")
            try:
                contact = self.driver.find_element_by_xpath("//span[@title=\""+contact_name+"\"]")
            except:
                print("Search Contact, Using Search Box")
                search_box_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]'
                search_box = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath(search_box_xpath))
                search_box.click()
                search_box.send_keys(contact_name)
                contact = self.driver.find_element_by_xpath("//span[@title=\""+contact_name+"\"]")
            contact.click()
            print("Contact Found")
            menu = self.driver.find_element_by_xpath("(//div[@title=\"Menu\"])[2]")
            menu.click()
            time.sleep(2)
            try:
                info = self.driver.find_element_by_xpath("//div[@title=\"Group info\"]")
            except:
                info = self.driver.find_element_by_xpath("//div[@title=\"Contact info\"]")
            info.click()
            time.sleep(5)
            media_xpath = '//span[text()="Media, Links and Docs"]'
            media = self.driver.find_element_by_xpath(media_xpath)
            media.click()
            time.sleep(5)
            check_boxes = self.driver.find_elements_by_class_name("_2Ry6_")
            check_boxes[0].click()
            time.sleep(2)

            print("==================Getting Images====================")
            while True:
                try:
                    i = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
                    image_xpath ='//img[@class="rN9sv _2-V0A _3FXB1"]'
                    image = WebDriverWait(self.driver,20).until(lambda driver: self.driver.find_element_by_xpath(image_xpath))
                    image_src = image.get_attribute("src");
                    result = self.driver.execute_async_script("""
                        var uri = arguments[0];
                        var callback = arguments[1];
                        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
                        var xhr = new XMLHttpRequest();
                        xhr.responseType = 'arraybuffer';
                        xhr.onload = function(){ callback(toBase64(xhr.response)) };
                        xhr.onerror = function(){ callback(xhr.status) };
                        xhr.open('GET', uri);
                        xhr.send();
                        """, image_src)
                    if type(result) == int :
                        raise Exception("Request failed with status %s" % result)
                    final_image = base64.b64decode(result)
                    filename = 'images/'+str(i)+'.jpg'  # I assume you have a way of picking unique filenames
                    with open(filename, 'wb') as f:
                        f.write(final_image)
                        print("Saving "+filename+", Go To The Next Image")
                    time.sleep(2)
                    next_button = self.driver.find_element_by_xpath('//div[@class="KNt1E _2ucQa"]')
                    next_button.click()
                    time.sleep(2)
                except Exception as e:
                    try:
                        next_button = self.driver.find_element_by_xpath('//div[@class="KNt1E _2ucQa"]')
                        next_button.click()
                        time.sleep(2)
                    except Exception as err:
                        print("All images scraped!")
                        print("Finish")
                        close_image_button = self.driver.find_element_by_xpath('//div[@title="Close"]')
                        close_image_button.click()
                        break
                    print("error")
                    print(e)
        except Exception as e:
            print(e)
            self.driver.quit()

    def quitDriver(self):
        print("Quit")
        self.driver.quit()

scraper = Scraper()

while True:
    print("Logged In")
    print("===================Menu=================")
    print("1. Scrape Images From Contact")
    print("2. Quit")
    print("========================================")
    menu = input()
    print(menu)
    if menu == '1':
        scraper.scrapeImages()
    elif menu == '2':
        scraper.quitDriver()
        break



