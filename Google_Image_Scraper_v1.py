from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver #web driver is driving
import time
from PIL import Image
import requests
import io
import base64
import string
import os
import io

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

if __name__ == '__main__':
    print("Welcome to the Not a Virus Google Image Scraper. Remember to run this program with Administrator privalleges.")

    query_list = get_queueries()

    for i in query_list:
        print(i)
        print()