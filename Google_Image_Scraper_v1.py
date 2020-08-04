from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
import time
from PIL import Image
import requests
import io
import base64
import string
import os

def get_queueries():

    print("Please enter your Google Image Search Query (Lim 250 character). Enter 'TERMINATE' when done.")
    print("")
    query_list = []
    while(True):
        query = input("Enter your query: ")
        print("")
        if query == "TERMINATE":
            return query_list
        else:
            query_list.append(query)

def get_num():

    print("Please enter the number of images you want from all of the searches (num>=1)")
    while(True):
        num = input("Enter your number: ")
        if(int(num) >= 1):
            return int(num)
        else:
            continue

def get_dicrectory():

    print("Please enter where you would like to store the images. Each query will be given its own file. Press [enter] to place in the working directory")
    print()
    directory = input("Enter your directory: ")
    return directory




def get_URLs(query_list, num_images, driver):

    driver.get("https://www.google.com/imghp?hl=en&tab=wi&authuser=0&ogbl")
    for query in query_list:
        url = []
        print("Getting images under: " + query)
        print()

        #Preform search query 
        search = driver.find_element_by_name('q')
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(5)

        #Ensure proper number of images are loaded
        image = driver.find_elements_by_css_selector("img.Q4LuWd") 
        print("Found " + str(len(image)))
        time.sleep(1)
        while len(image) < num_images:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            image = driver.find_elements_by_css_selector("img.Q4LuWd")
            time.sleep(1)
            print("Found " + str(len(image)))

        #Add Image URL's to url list 
        for num in range(num_images):   
            url.append(image[num].get_attribute('src'))
        
        #Retrieve images from URL list for the Query 
        retrieve_Images(url, query)
        image.clear()
        url.clear()
        driver.find_element_by_name('q').clear()

def retrieve_Images(url, query):
    
    counter = 0
    #Iterate through URL list to pull out images
    for num in range(len(url)):
        #Case 1: Image stored in base64
        try:
            #print(url[num])
            url_string = url[num].split(',')[1]
            
            #print(url_string)
            file_name = query + "_" + str(counter) + '.png'
            #save_Images(url_string, file_name, directory, 1)
            with open(file_name, "wb") as fh:
                fh.write(base64.b64decode(url_string))
            print(file_name)  
        except:
            print("Error:" + query + " " + str(num) + " not stored in Base64 formatting. Attepmting to pull a request for the image.")
            #Case 2: Image does not exist in base64. Request the image from the webpage. 
            try: 
                driver.get(url[num])
                image = driver.find_element_by_tag_name('img')
                src = image.get_attribute('src')
                file_name = query + "_" + str(counter) + '.png'
                img = requests.get(src)
                #save_Images(img, file_name, directory, 0)
                with open(file_name, "wb") as fh:
                    fh.write(img.content)
                print(file_name)
            except:
                #Handling case of if image URL returned as Null
                if url[num] is None:
                    continue
                #Handling case if image URL request failed
                else:
                    print("Failed to reach url: " + url[num])
                    print(url[num])
                    continue
        time.sleep(0.5) #Rest period to avoid blockage by Google
        counter += 1
    print("Saved " + str(counter) + " " + query + " Images")
    print()
    
def save_Images(img, file_name, base_64_bin):
    
    if base_64_bin == 1:
       with open(file_name, "wb") as fh:
            fh.write(base64.b64decode(img))
        #print(file_name)
    else:
        with open(file_name, "wb") as fh:
            fh.write(img.content)
        #print(file_name)
                  
if __name__ == '__main__':
    PATH = ''#place path chrome_driver.exe here in your/path/here format
    
    driver = webdriver.Chrome(PATH)
   
    print("Welcome to the Not a Virus Google Image Scraper. Remember to run this program with Administrator privalleges.")

    #Get needed information 
    query_list = get_queueries()
    num_images = get_num()
    directory = get_dicrectory()

    #Begin process of getting Images
    get_URLs(query_list, num_images, driver)
    
    driver.quit()