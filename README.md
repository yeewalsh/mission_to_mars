# Mission to Mars

Web-scraping data about Mars from multiple sources using Python, BeautifulSoup, splinter, mongoDB, html, Bootstrap, and Flask.

## Description

The flask app includes up-to-date information about Mars including:

* Most recent Mars news article: 
    * title and summary
    * source: https://redplanetscience.com/
* Most recent image of Mars
    * source: https://spaceimages-mars.com
* Chart of data comparing Mars and Earth
    * source: https://galaxyfacts-mars.com
* Full resolution images of Mars' hemispheres
    * source: https://marshemispheres.com/

## Challenges

The Mars hemisphere full-resolution links on the marshemispheres.com webpage were added using generic html tags which were present in many other locations of the html. This made it difficult to isolate the specific full image, and required drilling down multiple times using the html.find function. 

Working in Flask is time-consuming as you need to re-run the flask app each time you adjust the index.html template file. 

# Bootstrap 3 components used

1. All objects optimized for smart phones and tablets
2. "Scrape New Data" button changed to orange to match Mars colors
3. "Mars Facts" header centered and bolded

