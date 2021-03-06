# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# set function to 'scrape_all' using below code and add mongo connection
def scrape_all():
    
    # initialize headless driver for deployment / splinter setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # set variables from mars_news function to pull it's data
    news_title, news_paragraph = mars_news(browser)
    
    # run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    

    # stop the webdriver and return data
    browser.quit()
    return data


# function to scrape mars news site

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
    
        slide_elem = news_soup.select_one('div.list_text')

        # use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    # return for mars_news function: used instead of original print statements
    return news_title, news_p


# function to scrape the featured image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add error handling for AttributeError
    try:
    
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None
    
    # Use the base url to create an aboslute url:
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url



# function to scrape the mars info table
def mars_facts():
    
    # add a try/ecxept for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
    
    # assign columns and set index of df
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # convert df to HTML format, add bootstrap
    return df.to_html()


# function to scrape the hemisphere images
def hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_img_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')


    hemis = hemisphere_soup.find('div', class_="item")

    # use for loop to iterate through the hemispheres
    for x in range(0,4):
        hemispheres = {}
        
        full_image_elem = hemis.find('img', class_='thumb')
        
        # click on the name of the hemisphere to load page w/ full image
        full_image_elem = browser.find_by_tag('h3')[x]
        full_image_elem.click()
        
        # parse the new page html data
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        # find the Downlaods box text and locate the <a /> tag w/ the link
        img_elem = img_soup.find('div', class_='downloads')
        img_url_rel = img_elem.find('a').get('href')
        img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url_rel}'
        
        
        # find the Downloads header and get the hemisphere title
        title = img_soup.find('h2', class_="title").get_text()
        
        hemispheres = {
            'img_url': img_url, 
            'title' : title
        }
        
        hemisphere_img_urls.append(hemispheres)

        
        browser.back()

    return hemisphere_img_urls



if __name__ == "__main__":
    # if running as a script, print scraped data
    print(scrape_all())