""" Web scraper to extract image from a E-shopping website such as Sarenza (shoes) -- NO PROXIES"""

from bs4 import BeautifulSoup
import requests
import urllib.request
import sys
import os
import traceback
import re
import time

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}



def ParsePage(url):
    print(url)
    #Extract the response of the url
    html = requests.get(url, headers=headers)

    #Create a Beautiful BeautifulSoup object
    soup = BeautifulSoup(html.text, "lxml")

    #Get to the product page
    links = soup.findAll("a", {"class":"product-link"}, href = True)
    i = 0
    for product in links:
        i+=1
        link_to_product = product['href']
        Name = ("http://www.sarenza.com" + link_to_product)
        html_page = requests.get(Name)
        soupProduct = BeautifulSoup(html_page.text, 'lxml')
        print("Scraping image no", i)
        for img in soupProduct.findAll("img", {"class":"zoom progressive"}, {"width": "480"}):
            #time.sleep(1) Not very nice but too long to scrap for women shoes
            types = soupProduct.findAll("div", {"class":"product-details"})
            type = types[0].tr.text
            if (type != "Sport" and type != "Sport Randonnée / Outdoor"):
                type = type[5:]
            elif type == "Sport Randonnée / Outdoor":
                type = "Randonnée"
            elif type == "Sport Running / Trail":
                type = "Running"
            elif type == "Sport Tennis":
                type = "Tennis"
            elif type == "Sport Skate":
                type = "Skate"
            elif type == "Sport Football":
                type = "Football"
            elif type == "Sport Basketball":
                type = "Basketball"
            elif type == "Sport Indoor / Sport en salle":
                type = "Indoor"
            elif type == "Sport Sports aquatiques":
                type = "Tongs"


            url_img = img['src']
            url_img = url_img[:-7]
            url_img = url_img + "5"
            url_img = url_img + "0"
            url_img = url_img + "0"
            url_img = url_img + ":"
            url_img = url_img + "3"
            url_img = url_img + "3"
            url_img = url_img + "3"
            if type != " ":
                file_name = "/media/arthur/DATA/Databases/ScrapingShoesF/" + type + "/" + url_img.split('/')[-1]
            else:
                file_name="/media/arthur/DATA/Databases/ScrapingShoesF/" + url_img.split('/')[-1]
            try:
                f = open(file_name, 'wb')
                file_path = os.path.join("home/arthur/Pictures", file_name)
                urllib.request.urlretrieve(url_img, file_path)
                f.close()
            except FileNotFoundError:
                print("Catégorie non reconnue")



            # Try to not look like a bot, create a fake request






if __name__ == '__main__':
    #website = "https://www.sarenza.com/store/product/gender/list/view?gender=1&index=0&count=700"
    #ParsePage(website)
    debut = 18684
    for i in range(30):
        website = "https://www.sarenza.com/store/product/gender/list/view?gender=1&index=" + str(700*i + debut) + "&count=700"
        ParsePage(website)
