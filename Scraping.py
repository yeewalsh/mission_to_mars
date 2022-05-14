# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# splinter setup
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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
        slide_elem.find('div', class_='content_title')


        # use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    # return for mars_news function: used instead of original print statements
    return news_title, news_p


### Featured Images

# declare and define the function
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

### Mars Info Table

# define the function
def mars_facts():
    
    # add a try/ecxept for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
    
    # assign columns and set index of df
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # convert df to HTML format, add bootstrap
    return df.to_html()

browser.quit()

