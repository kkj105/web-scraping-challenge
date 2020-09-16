from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests 

from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    news_title, news_p = news(browser)
    featured_image_url = image(browser)
    mars_facts = facts()
    hems_list = hemispheres(browser)
    data = {}

    data["mars_news"] = news_title
    data["mars_text"] = news_p

    data["featured_image"] = featured_image_url

    data["mars_facts"] = mars_facts

    data["mars_hems"] = hems_list

    
    

    return data

def news(browser):
    # URL of NASA page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Retrieve the parent divs for all articles
    results = soup.find_all('li', class_="slide")

    news_title =  results[0].find('div', class_='content_title').text
    news_p = results[0].find('div', class_='article_teaser_body').text

    return news_title, news_p

def image(browser):
    # URL of JPL page to be scraped
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    
    # Navigate to id for button "Full Image" & click
    browser.find_by_id('full_image').click()

    #Click button "More Info"
    browser.links.find_by_partial_text('more info').click()

    # Retrieve Featured image from page
    soup = BeautifulSoup(browser.html, "html.parser")

    featured_image_url = f"https://www.jpl.nasa.gov{soup.find('img', class_='main_image')['src']}"
    
    return featured_image_url

def facts():
    mars_facts = pd.read_html('https://space-facts.com/mars/')[0]
    mars_facts.columns=["Description", "Data"]
    mars_facts.set_index("Description", inplace=False)
    
    return mars_facts.to_html()

def hemispheres(browser):
    # URL of Mars hemispheres page to be scraped
    mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres)
    
    # Navigate to Cerberus Hemisphere link & click
    hemispheres = browser.find_by_css('h3')
    hems_list =[]


    for hemisphere in range(len(hemispheres)):
        mars_hems_dict = {}
        #print(title)
        title = browser.find_by_css('a.product-item h3')[hemisphere].text
        # create empty dict to store title & URL , then append dicts to larger list
        mars_hems_dict["title"]= title
        browser.find_by_css('a.product-item h3')[hemisphere].click()
        
        # Navigate to image download 
        mars_image = browser.find_by_text('Sample').first['href']
        # store img in dict
        mars_hems_dict["image"]=mars_image
        # store dictionary items into hems_list
        hems_list.append(mars_hems_dict)
        
        browser.back()
    
    return hems_list


    