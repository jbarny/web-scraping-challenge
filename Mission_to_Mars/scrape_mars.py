def scrape():

    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import time
    import pandas as pd
    import requests

    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    mars_info = {}

    ##### NASA Mars News #####
    
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)

    html_news = browser.html
    soup_news = bs(html_news, "html.parser")

    news_title = soup_news.find("div", class_="content_title").text
    news_p = soup_news.find("div", class_="article_teaser_body").text

    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p

    ##### JPL Mars Space Images - Featured Image #####

    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")

    html_img = browser.html
    soup_img = bs(html_img, "html.parser")

    featured_image = soup_img.find("figure").find("a")["href"]

    featured_image_url = f"https://www.jpl.nasa.gov{featured_image}"

    #print(featured_image_url)

    mars_info["featured_image_url"] = featured_image_url


    ##### Mars Weather #####

    url_twt = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url_twt)

    soup_twt = bs(response.text, "html.parser")

    mars_weather = soup_twt.find("div", class_="js-tweet-text-container").text.strip()

    mars_info["mars_weather"] = mars_weather

    ##### Mars Facts #####

    url_facts = "https://space-facts.com/mars/"
    facts = pd.read_html(url_facts)
    facts_df = facts[0]
    facts_df.columns = ["description", "value"]
    facts_df = facts_df.set_index("description")
    facts_html = facts_df.to_html().strip()

    mars_info["facts_html"] = facts_html

    ##### Mars Hemispheres #####

    url_astro = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_astro)

    html_astro = browser.html
    soup_astro = bs(html_astro, "html.parser")

    hemisphere_image_urls = []

    hemis = soup_astro.find_all("div", class_="description")

    for hemi in hemis:
        title = hemi.find("h3").text
        next_page = hemi.find("a")["href"]
        browser.visit(f"https://astrogeology.usgs.gov{next_page}")
        html_hemi = browser.html
        soup_hemi = bs(html_hemi, "html.parser")
        img_url = soup_hemi.find("div", class_="downloads").find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    mars_info["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_info