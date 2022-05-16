# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)



# set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')



# use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an aboslute url:
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Info Table

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df.to_html()


# # D1: Scrape High-Resolution Mars' Hemisphere Images

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemisphere_soup = soup(html, 'html.parser')


hemis = hemisphere_soup.find('div', class_="item")

# use for loop to iterate through the tags
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
    
    hemisphere_image_urls.append(hemispheres)

    
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()


