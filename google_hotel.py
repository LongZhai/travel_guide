import time
from selenium import webdriver
from operator import itemgetter
import calendar
import sys


class google_hotel():
    def __init__(self, location):
        self.location = location

    '''
    open chrome and search hotels near the perfect accommodation location in given travelling date
    '''
    def hotel_list(self, check_in, check_out):
        driver = webdriver.Chrome('/Users/logan/Downloads/Expedia-Scraping-Code-for-prices-master/chromedriver')  # Optional argument, if not specified will search path.
        driver.get('https://www.google.ca/maps')
        time.sleep(3) # Let the user actually see something!
        search_box = driver.find_element_by_id('searchboxinput')
        search_box.send_keys(self.location)
        search = driver.find_element_by_id('searchbox-searchbutton')
        search.click()
        time.sleep(3)
        search_box.clear()
        search_box.send_keys('hotel')
        search.click()
        time.sleep(5)
        search_date = driver.find_element_by_class_name("widget-pane-date-picker-label")
        search_date.click()
        # search_date = driver.find_element_by_class_name('widget-pane-date-picker-label')
        # search_date.click()
        the_month_on_cal, cal_year = driver.find_element_by_xpath("//td[@class='goog-date-picker-monthyear']").text.split(" ")
        curr_month = time.strptime(the_month_on_cal, '%B').tm_mon
        next_month = driver.find_element_by_css_selector(".goog-date-picker-btn.goog-date-picker-nextMonth")
        checkin_month = check_in[1] if curr_month <= check_in[1] and float(cal_year)<=check_in[0] else check_in[1]+12
        if curr_month > checkin_month:
            # pri_month = driver.find_element_by_css_selector(".goog-date-picker-btn.goog-date-picker-nextMonth")
            print("invalid check in month")
            driver.quit()
            sys.exit(1)
        while curr_month < checkin_month:
            curr_month += 1
            next_month.click()
        time.sleep(3)
        try:
            date = driver.find_element_by_xpath("//td[@aria-label='{} {}']".format(check_in[2],calendar.month_abbr[check_in[1]]))
            date.click()
            date_2 = driver.find_elements_by_xpath("//td[@aria-label='{} {}']".format(check_out[2],calendar.month_abbr[check_out[1]]))
            date_2[1].click()
        except Exception:
            print("invalid check in date")
            driver.quit()
            sys.exit(1)
        time.sleep(5)
        hotel_list = []
        for x in driver.find_elements_by_class_name('section-result-text-content'):
            content = x.text
            name = content[:content.find('\n')]
            try:
                price_index =content.find('$')+1
                price_end = content[price_index:].find('\n') + len(content[0:price_index:])
                price = float(content[price_index:price_end])
                score = float(content[content.find('$') - 4:content.find('$')-1])
            except Exception:
                print("no price information for ", name)
                score = 0
                price = 0
            hotel_list.append((name, price, score))
        hotel_list.sort(key=itemgetter(1,2))
        hotel_sort_score = hotel_list.copy()
        hotel_sort_score.sort(key=itemgetter(2), reverse=True)
        new_list = []
        for x in hotel_list:
            position = (hotel_list.index(x) + hotel_sort_score.index(x))/2
            new_list.append((position, x))
        new_list.sort(key=itemgetter(0))
        print("----------the hotel recommendation : ----------")
        new_list = new_list[:5] if len(new_list) >= 5 else new_list
        for i in new_list:
            print("name: ",i[1][0], " price: ", i[1][1], " review score: ", i[1][2])
        driver.quit()
        # driver.minimize_window()

