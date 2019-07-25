from time import sleep
from selenium import webdriver
from pyquery import PyQuery as pq
import csv  
import os
import requests
from PIL import Image
#from io import StringIO
from io import open as iopen


class ScrapeCard():
    def __init__(self):
        self.url_to_scrape = 'http://www.123greetings.com/thank_you/everyday/'
        self.all_items = []
   
    # Open chromedriver
    def start_driver(self):
        self.driver = webdriver.Chrome()
        sleep(3)

    # Close chromedriver
    def close_driver(self):
        self.driver.quit()

    # Tell the browser to get all pages
    def get_page(self, url):
        print('getting web page...')
        self.driver.get(url)       
        sleep(2)
        
    ##SCROLL DOWN FOR THE FULL PAGE TO LOAD 
    def scroll_page(self):
        lastHeight = 0
        currentHeight = 0
        
        while True:
            currentHeight = self.driver.execute_script(" return document.body.scrollHeight")
            if(currentHeight > lastHeight):
                lastHeight = currentHeight
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")    
            else:
                break
       
    def path_leaf(self, path):
        filename = os.path.basename(path)
        return filename
          
    def grab_list_items(self, doc):
        liDoc = doc('#div_thumbs > li').items()
        
        for eachitem in liDoc:
            one_card = self.process_elements(eachitem)
            self.all_items.append(one_card)
          
    def process_elements(self, item):
            one_card = []
            
            img_src = item('div > a > img').attr("src")
            pic_url_list.append(img_src)    
            path = item("h2 > a").attr("href")
            filename = self.path_leaf(path)
            link = self.url_to_scrape + filename
            title = item("h2").text()
            content = item("p.std").text()
            rated = item("p.card-data.sp-sm").text()
            if(rated[:5] != 'Rated'):
                rated = ''
            one_card.append(title)
            one_card.append(link)
            one_card.append(content)
            one_card.append(rated[6:9])
            return one_card   
    
    
    def parse(self):
        nextPage = ''
        html = ''
       
        self.start_driver()
        pageNo = 1
        self.get_page(self.url_to_scrape)
        self.scroll_page()
        ## Try to allow time for the full page to load the lazy way
        sleep(5)      
          
       
        while True:
            html = self.driver.find_element_by_css_selector("*").get_attribute("outerHTML")
            doc = pq(html)
            self.grab_list_items(doc)
            pageNo += 1
            nextPage = '//a[@title="Go to page {:s}"]'.format(str(pageNo))
            print(nextPage)
            try:
                self.driver.find_element_by_xpath(nextPage).click()
           
            except Exception:
                break

            self.scroll_page()
                ## Try to allow time for the full page to load the lazy way
            sleep(3)    
        
        self.close_driver()
        print("Get total cards: " + str(len(self.all_items)))
            
        return self.all_items
        

# MAIN PROGRAM
# items_list = [["Title","link","Content","Rated"]]
items_list = [["","","",""]]
pic_url_list = []

Cards_Info = ScrapeCard()
items_list = Cards_Info.parse()   # retrieve card information, items_list = [["Title","link","Content","Rated"]]

index = 0
for i in range(len(pic_url_list)):
    img_src = ''
    
    img_src = str(pic_url_list[index])
    # Send an HTTP GET request, get and save the image from the response
    image_object = requests.get(img_src)
    image_object.content
 #   image = Image.open(StringIO(image_object.content)) 
    my_path = 'D:/Python_Project/img/' + os.path.basename(img_src)
                      
    with iopen(my_path, 'wb') as file:
        file.write(image_object.content)
   
    index += 1
    

print("Get total thumbnails: " + str(len(pic_url_list)))
      
        
# store the retrieved cards data into .csv file  
for item in items_list:
    oneCard = []
    
    with open("Thank_You_Cards1.csv", "w") as fOut:
        csvOut = csv.writer(fOut)
        csvOut.writerow(["Title","link","Content","Rated"])
        csvOut.writerows(items_list)
 

    
