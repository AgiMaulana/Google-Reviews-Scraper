from selenium import webdriver
import time
import pandas as pd


def save(rate, review):
    df = pd.read_csv('reviews.csv')
    rates, reviews = df.rate.values.tolist(), df.review.values.tolist()
    if type(rate) == list:
        rates.extend(rate)
        reviews.extend(review)
    else:
        rates.append(rate)
        reviews.append(review)
    pd.DataFrame({'rate': rates, 'review': reviews}).to_csv('reviews.csv', index=False)


def extract(driver, loading_time):
    dialog_box = driver.find_element_by_xpath('//div[@class="review-dialog-list"]')
    i = 0
    while i < 20:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', dialog_box)
        time.sleep(loading_time)
        i += 1

    user_review_containers = driver.find_elements_by_xpath('//div[@class="WMbnJf gws-localreviews__google-review"]')
    rates, reviews = [], []
    for container in user_review_containers:
        rate_score = container.find_element_by_xpath('//div[@class="PuaHbe"]').find_element_by_tag_name(
            'span').get_attribute('aria-label')
        rating = rate_score[len('Diberi nilai'):len('Diberi nilai') + 4].strip()
        rating = round(float(rating.replace(',', '.')))
        print()
        print(rate_score)
        print(rating)
        try:
            container.find_element_by_xpath('//a[@class="fl review-more-link"]').click()
        except:
            pass
        review = container.find_element_by_class_name('Jtu6Td').text
        print(review)

        if rating != 3:
            rates.append(rating)
            reviews.append(review)

    return rates, reviews


def scrap(keyword):
    loading_time = 3

    url = 'https://google.co.id/search?q=' + keyword
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(loading_time)
    try:
        all_reviews_button = driver.find_element_by_link_text('Lihat semua ulasan Google')
        all_reviews_button.click()
        time.sleep(loading_time)
        sorting_spinner = driver.find_element_by_class_name('S7TGef')
        sorting_spinner.click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[4]/div').click() # lower to higher
        time.sleep(loading_time)
        rates, reviews = extract(driver, loading_time)
        save(rates, reviews)

        sorting_spinner = driver.find_element_by_class_name('S7TGef')
        sorting_spinner.click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[3]/div').click() # higher to lower
        time.sleep(loading_time)
        rates, reviews = extract(driver, loading_time)
        save(rates, reviews)
    except:
        pass


scrap('saung mang engking cibubur')
