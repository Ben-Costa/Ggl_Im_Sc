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

def get_URLs(query_list, num_images, driver, directory):

    driver.get("https://www.google.com/imghp?hl=en&tab=wi&authuser=0&ogbl")
    for query in query_list:
        url = []
        print("Getting images under: " + query)
        print()

        # Preform search query 
        search = driver.find_element_by_name('q')
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        time.sleep(5)

        # Ensure proper number of images are loaded
        image = driver.find_elements_by_css_selector("img.Q4LuWd") 
        print("Found " + str(len(image)) + "Images")
        time.sleep(5)
        while len(image) < num_images:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            image = driver.find_elements_by_css_selector("img.Q4LuWd")
            time.sleep(5)
            print("Found " + str(len(image)) + "Images")

        # Add Image URL's to url list 
        for num in range(num_images):   
            url.append(image[num].get_attribute('src'))
        
        # Retrieve images from URL list for the Query 
        retrieve_Images(url, query, directory)
        image.clear()
        url.clear()
        driver.find_element_by_name('q').clear()
        time.sleep(5)

def retrieve_Images(url, query, directory):
    
    counter = 0
    # Iterate through URL list to pull out images
    for num in range(len(url)):
        # Case 1: Image stored in base64
        try:
            url_string = url[num].split(',')[1]
            file_name = query + "_" + str(counter) + '.png'
            save_Images(url_string, file_name, directory, 1, query) 
        except:
            print("Error:" + query + " " + str(num) + " not stored in Base64 formatting. Attepmting to pull a request for the image.")
            # Case 2: Image does not exist in base64. Request the image from the webpage. 
            try: 
                driver.get(url[num])
                image = driver.find_element_by_tag_name('img')
                src = image.get_attribute('src')
                file_name = query + "_" + str(counter) + '.png'
                img = requests.get(src)
                save_Images(img, file_name, directory, 0, query)
            except:
                #Handling case of if image URL returned as Null
                if url[num] is None:
                    continue
                # Handling case if image URL request failed
                else:
                    print("Failed to reach url: " + url[num])
                    continue
        time.sleep(0.5) # Rest period time. Can be changed to speed up process. 
        counter += 1
    print("Saved " + str(counter) + " " + query + " Images")
    print()
    
def save_Images(img, file_name, directory, base_64_bin, query):
    
    # Case 1: If a directory to save was not given select the working directory
    if(directory == ""):
        folder_path = os.path.join(os.getcwd(), query)
        # Check if directory path exists
        if(not os.path.exists(folder_path)):
            os.makedirs(folder_path)
        folder_path = os.path.join(folder_path, file_name)
        # Case 1: Base64 conversion
        if base_64_bin == 1:
            with open(folder_path, "wb") as fh:
                fh.write(base64.b64decode(img))
        # Case 2: Request conentet 
        else:
            with open(folder_path, "wb") as fh:
                fh.write(img.content)
    # Case 2: Directory was given
    else:
        folder_path = os.path.join(directory, query)
        # Check if directory path exists
        if(not os.path.exists(folder_path)):
            os.makedirs(folder_path)
        folder_path = os.path.join(folder_path, file_name)
            # Case 1: Base64 conversion
        if base_64_bin == 1:
            with open(folder_path, "wb") as fh:
                fh.write(base64.b64decode(img))
        # Case 2: Request conentet 
        else:
            with open(file_name, "wb") as fh:
                fh.write(img.content)

if __name__ == '__main__':
    PATH = '/mnt/c/Users/bc234/Coding_Repo/Web_Scrape/chromedriver.exe'#place path chrome_driver.exe here in your/path/here format
    
    driver = webdriver.Chrome(PATH)
   
    print("Welcome to the Not a Virus Google Image Scraper. Remember to run this program with Administrator privalleges.")

    #Get needed information 
    query_list = get_queueries()
    num_images = get_num()
    directory = get_dicrectory()

    #Begin process of getting Images
    get_URLs(query_list, num_images, driver, directory)
    
    print("Process Complete")
    driver.quit()