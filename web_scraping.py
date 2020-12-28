import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from PIL import Image
import io
from selenium import webdriver
import time
import os
import json



def scraper(searchString, NO_OF_PAGES):
  Product_dict = {}
  for i in range(NO_OF_PAGES):
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString + "&page={}".format(i)
    uClient = uReq(flipkart_url)
    flipkartPage = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkartPage, "html.parser")
    bigboxes = flipkart_html.findAll("a", {"class": "IRpwTa"})
    for item in bigboxes:
      title = item['title']
      link = "https://www.flipkart.com" + item['href']
      Product_dict[title] = {'title': title, 'URL': link}
  return Product_dict

def run(PRODUCTS_LIST,NO_OF_PAGES,DEST_FOLDER, JSON_PATH):
    total_prod_data = {}
    for product in PRODUCTS_LIST:
        print(" Start Scraping", product)
        prod_data = scraper(product, NO_OF_PAGES)
        for k, v in prod_data.items():
          driver.get(v['URL'])
          time.sleep(3)
          try:
            rating_tag = driver.find_elements_by_xpath("//div[contains(@class,'_3LWZlK _3uSWvT')]")
            rating = rating_tag[0].get_attribute('textContent')
            prod_data[k]['rating'] = round(float(rating))
          except:
            continue
          try:
            imgResults = driver.find_elements_by_xpath("//img[contains(@class,'_2r_T1I _396QI4')]")
            imgResults[0].click()
            time.sleep(2)
            url = imgResults[0].get_attribute('src')
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            pth = k + '.jpg'
            file_path = os.path.join(DEST_FOLDER, pth)
            with open(file_path, 'wb') as f:
              image.thumbnail((350, 300))
              image.save(f, "JPEG", quality=85)
          except:
            continue
        total_prod_data.update(prod_data)

    with open(JSON_PATH, "w") as outfile:
      json.dump(total_prod_data, outfile)

if __name__ == "__main__":
  # Configuration variables
  BASEPATH = os.path.abspath(os.getcwd())
  NO_OF_PAGES = 10
  PRODUCTS_LIST = ['mens%20jeans', 'mens%20shirts','watch']
  DEST_FOLDER = os.path.join(BASEPATH, 'data', 'dataset', 'prod_data')
  WEBDRIVER_PATH = os.path.join(BASEPATH, 'chromedriver.exe')
  JSON_PATH = os.path.join(BASEPATH, 'data', 'dataset','json_data', 'ProductsData.json')

  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')
  driver = webdriver.Chrome(WEBDRIVER_PATH, chrome_options=chrome_options)

  run(PRODUCTS_LIST, NO_OF_PAGES, DEST_FOLDER, JSON_PATH)
  print("Scraping Completed")