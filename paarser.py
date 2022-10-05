from time import sleep
import json

import selenium.common
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class Parser:

    def __init__(self):
        self.driver = self.__define_driver()
        self.requests = [['Миг-21', '', '0']]
        # self.buf = []
        self.i = 0
        self.running = False
        print('initialized')

    def __define_driver(self):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--disable-extensions")

        driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        driver.get('https://www.avito.ru/moskva_i_mo?q=%D0%9C%D0%98%D0%93-21&s=104')
        sleep(5)
        return driver

    '''def add_request(self, request):
        """
        self.buf.append(request)
        print('parser: request added')
        """
        with open('buffer.txt', 'a') as buf:
            buf.writelines([request, '\n'])'''

    '''def __check_requests(self):
        print('checking new requests')
        for request in self.buf:
            self.requests.append([request, self.check_by_name(request)])
        self.buf.clear()'''

    def __check_requests(self):
        print('checking new requests')
        with open('buffer.txt', 'r', encoding='utf8') as buf:
            requests = buf.read().splitlines()
        for request in requests:
            print(request)
            try:
                d = json.loads(request)
                self.requests.append([d['request'], self.check_by_name(d['request']), d['user_id']])
            except json.decoder.JSONDecodeError:
                continue
        with open('buffer.txt', 'r+') as buf:
            buf.truncate()

    def __check_next(self):
        print(self.requests)
        print(self.i)
        print('checking next')
        cur_link = self.check_by_name(self.requests[self.i][0])
        if cur_link != self.requests[self.i][1]:
            self.__send_ad(cur_link)
            self.requests[self.i] = [self.requests[self.i][0], cur_link, self.requests[self.i][2]]
        self.i = (self.i + 1) % len(self.requests)

    def check_by_name(self, request):
        textfield = None
        try:
            textfield = self.driver \
                .find_element(By.XPATH,
                              '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div/label[1]')
        except selenium.common.NoSuchElementException:
            try:
                textfield = self.driver \
                    .find_element(By.XPATH,
                                  '/html/body/div[1]/div/div[2]/div/div[3]/div/div[2]/div/div/div/label[1]')
            except selenium.common.NoSuchElementException:
                textfield = self.driver \
                    .find_element(By.XPATH,
                                  '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div/div/label[1]/input')

        textfield.send_keys(Keys.CONTROL, 'a')
        textfield.send_keys(Keys.DELETE)
        textfield.send_keys(request)
        try:
            self.driver \
                .find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/button') \
                .click()
        except selenium.common.NoSuchElementException:
            self.driver \
                .find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[3]/button') \
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
        with open('output.txt', 'a', encoding='utf8') as out:
            d = {'request': self.requests[self.i][0],
                 'link': link,
                 'user_id': self.requests[self.i][2]}
            out.write(str(d) + '\n')

    # Дальше добавляю буффер, в который телеболт будет закидывать новые предложения
    # и считывание этих предложений парсером.

    #  Типа жизненный цикл парсера:


