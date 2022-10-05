from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Parser:

    def __init__(self):
        self.driver = self.__define_driver()
        self.requests = []
        self.buf = []
        self.i = 0
        self.running = False
        print('initialized')

    def __define_driver(self):
        options = Options()
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        #options.add_argument("--disable-extensions")

        driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        driver.get('https://www.avito.ru/moskva_i_mo?q=%D0%9C%D0%98%D0%93-21&s=104')
        sleep(5)
        return driver

    def add_request(self, request):
        self.buf.append(request)
        print('parser: request added')

    def __check_requests(self):
        print('checking new requests')
        for request in self.buf:
            self.requests.append([request, self.check_by_name(request)])
        self.buf.clear()

    def __check_next(self):
        print('checking next')
        cur_link = self.check_by_name(self.requests[self.i][0])
        if cur_link != self.requests[self.i][1]:
            self.__send_ad(cur_link)
            self.requests[self.i] = [self.requests[self.i][0], cur_link]
            self.i = (self.i + 1) % len(self.requests)

    def check_by_name(self, request):
        textfield = self.driver.find_element(By.CLASS_NAME, 'suggest-input-Wpgla')
        textfield.send_keys(Keys.CONTROL, 'a')
        textfield.send_keys(Keys.DELETE)
        textfield.send_keys(request)
        self.driver.find_element(By.CLASS_NAME, 'form-part-button-_NYZb') \
            .click()
        sleep(5)
        link = self.driver.find_elements(By.CLASS_NAME, 'iva-item-content-rejJg')[0] \
            .find_element(By.XPATH, './/div[1]/a').get_attribute('href')
        return link

    def start(self):
        print('Parser started')
        self.running = True
        while self.running:
            self.__check_requests()
            self.__check_next()

    def __send_ad(self, link):
        print('Add sent,', link)

    # Дальше добавляю буффер, в который телеболт будет закидывать новые предложения
    # и считывание этих предложений парсером.

    #  Типа жизненный цикл парсера:
