

from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from logging.handlers import RotatingFileHandler
import logging
from datetime import datetime
import json
# from django.db import transaction, IntegrityError
import sys
# import django
import time
import mysql.connector
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawlapi.settings")
# django.setup()
# from core_app.serializers import SystemConfigSerializer
# from core_app.models import SystemConfig, Item, LogCrawl

LOGGER.setLevel(logging.WARNING)
logname = "debug.log"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#Load json data
data_json = None
with open('config.json') as config_file:
    data_json = json.load(config_file)
if data_json is None:
    logger.debug("data_json is undefined")
    sys.exit(1)

delay = 5
if sys.platform.startswith('linux'):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2})
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-setuid-sandbox")
    chromeOptions.add_argument("--remote-debugging-port=9222")  # this
    chromeOptions.add_argument("--disable-dev-shm-using")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_argument("--headless")

    driver = webdriver.Chrome(
        '/usr/lib/chromium-browser/chromedriver', chrome_options=chromeOptions)
else:
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2})
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-setuid-sandbox")
    chromeOptions.add_argument("--remote-debugging-port=9222")  # this
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(executable_path='./geckodriver/chromedriver.exe', chrome_options=chromeOptions)

url = 'https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3'


def click_to_element(driver, city, district):
    drd_location = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'location')))
    driver.execute_script("arguments[0].click();", drd_location)

    cities = driver.find_elements_by_class_name("search__location-items__item")
    for e in cities:
        if e.get_attribute("textContent") == city:
            driver.execute_script("arguments[0].click();", e)
            break
    districts = driver.find_elements_by_class_name(
        "search__location-items__item")
    for e in districts:
        if e.get_attribute("textContent").find(district) != -1:
            driver.execute_script("arguments[0].click();", e)
            break


def connect_db():
    return mysql.connector.connect(user=data_json["user"], password=data_json["pass"], host=data_json["host"], database=data_json["db"])

def fetch_all(query):
    try:
        cnx = connect_db()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query)
        list_data = cursor.fetchall()
    except Exception as e:
        print(e)
        logger.debug(e)
        list_data = None
    finally:
        cursor.close()
        cnx.close()
    return list_data


def check_exist(query, id):
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        cursor.execute(query, (id,))
        msg = cursor.fetchone()
        if not msg:
            return False
        return True
    except Exception as e:
        print(e)
        logger.debug(e)
        return True
    finally:
        cursor.close()
        cnx.close()


def save_article(dict_article, log_id):
    try:
        cnx = connect_db()
        cursor = cnx.cursor()
        placeholders = ', '.join(['%s'] * len(dict_article))
        columns = ', '.join(dict_article.keys())
        sql = "INSERT INTO tbl_data ( %s ) VALUES ( %s )" % (
            columns, placeholders)

        # valid in Python 3
        cursor.execute(sql, list(dict_article.values()))
        cursor.execute(
            """INSERT INTO tbl_log_crawl (log_id) VALUES (%s)""", (log_id,))
        cnx.commit()
    except Exception as e:
        print(e)
        logger.debug(e)
    finally:
        cursor.close()
        cnx.close()


while True:
    start_time = time.time()
    # lay du lieu config
    query = "select * from tbl_system_config"
    list_data = fetch_all(query)

    if list_data == None or len(list_data) == 0:
        time.sleep(delay)
        continue
    print(list_data)
    for data in list_data:
        # Xu ly click element
        driver.get(url)
        city = data['city']
        district = data['district']
        pages = data['total_page']
        try:
            click_to_element(driver, city, district)
        except Exception as e:
            print(e)
            continue

        base_url = driver.current_url
        print(base_url)
        for page in range(1, pages + 1):
            url_page = base_url + '?cp=' + str(page)
            driver.get(url_page)
            try:
                block_article = WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located((By.ID, 'list-box')))
                list_article = block_article.find_elements_by_class_name(
                    "list-item-container")
                links_hrefs = [link.find_element_by_tag_name(
                    'a').get_attribute('href') for link in list_article]
                for item in links_hrefs:
                    log_id = 'mb' + item.rsplit('-', 1)[-1]
                    query = "SELECT 1 FROM tbl_log_crawl WHERE log_id = %s"
                    if check_exist(query, log_id) == True:
                        continue

                    driver.get(item)

                    try:
                        # main block
                        block_article_detail = WebDriverWait(driver, delay).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detail-container__left')))
                        article = {}
                        article["url"] = item
                        # Lay anh
                        img_url = ''

                        # Neu la 1 anh
                        try:
                            image = block_article_detail.find_element_by_class_name('image-container__image')
                            img_url = image.get_attribute('src')
                        except NoSuchElementException:
                            pass
                        #Neu la slide anh
                        try:
                            images = block_article_detail.find_elements_by_class_name('slider__frame')
                            for image in images:
                                img_url += image.get_attribute('src') + '#'
                        except NoSuchElementException:
                            pass
                        article['images'] = img_url
                        
                        title = block_article_detail.find_element_by_css_selector(
                            'h1.title').text
                        article["title"] = title.encode('utf8')
                        # detail article
                        content_text = block_article_detail.find_element_by_class_name(
                            'body-container').text
                        article["description"] = content_text.encode('utf8')
                        # publisher mobile
                        try:
                            phone = block_article_detail.find_element_by_class_name(
                                'mobile-container__value').find_element_by_tag_name('span').get_attribute('mobile')
                        except NoSuchElementException:
                            phone = ''
                        article["publisher_mobile"] = phone
                        # price
                        try:
                            price = block_article_detail.find_element_by_class_name(
                                'price-container__value').text
                        except NoSuchElementException:
                            price = ''
                        article["price"] = price
                        # publish date
                        try:
                            article["publish_date"] = block_article_detail.find_element_by_css_selector(
                                'span.location-clock__clock').text
                        except NoSuchElementException:
                            pass
                        # publisher name
                        try:
                            publisher = block_article_detail.find_element_by_class_name(
                                'user-info__fullname').text
                        except NoSuchElementException:
                            publisher = ''
                        article["publisher"] = publisher
                        try:
                            property_element = block_article_detail.find_element_by_class_name(
                                'tect-content-block').find_elements_by_class_name('tech-item')

                            for div_row in property_element:
                                if div_row.text.strip().startswith('Địa'):
                                    article["address"] = div_row.find_element_by_xpath(
                                        'div[2]').text
                                elif div_row.text.strip().startswith('Diện'):
                                    article["square"] = div_row.find_element_by_xpath(
                                        'div[2]').text
                                elif div_row.text.strip().startswith('Pháp'):
                                    article["policy"] = div_row.find_element_by_xpath(
                                        'div[2]').text
                                elif div_row.text.strip().startswith('Hướng'):
                                    article["direction"] = div_row.find_element_by_xpath(
                                        'div[2]').text
                        except NoSuchElementException:
                            pass

                        article["created_date"] = datetime.now()
                        article["source"] = "muaban.net"
                        print(article)
                        try:
                            save_article(article, log_id)
                        except:
                            pass

                    except NoSuchElementException:
                        pass
                    finally:
                        time.sleep(0.5)

            except NoSuchElementException:
                pass
            finally:
                print("--- %s seconds ---" % (time.time() - start_time))
                time.sleep(delay)
