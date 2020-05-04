# -*- coding: utf-8 -*-
import os
import time
import requests
import scrapy
from scrapy_selenium import SeleniumRequest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from uptodate_parser.settings import (
    BASE_DIR, BASE_URL, SEARCH_URL, LOGIN_URL, USERNAME, PASSWORD,
    JSON_LOGIN_URL
)


class UptodateSpider(scrapy.Spider):
    name = 'uptodate'
    allowed_domains = ['uptodate.com']
    start_urls = [
        # 'https://www.uptodate.com/contents/overview-of-general-medical-care-'
        # 'in-nonpregnant-adults-with-diabetes-mellitus?search=diabetis&source'
        # '=search_result&selectedTitle=1~150&usage_type=default&display_rank=1'
        # '#H15053957'
        LOGIN_URL
        # JSON_LOGIN_URL
    ]

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        executable_path=os.path.join(BASE_DIR, '../drivers/geckodriver'),
        options=options
    )

    def start_requests(self):
        # return [
        #     scrapy.FormRequest(
        #         url=LOGIN_URL,
        #         formid='loginForm',
        #         formname='loginForm',
        #         clickdata={'id': 'btnLoginSubmit'},
        #         formdata={
        #             'userName': USERNAME, 'password': PASSWORD,
        #             'saveUserName': 'true', 'isSubmitting': 'true',
        #             'loginText': 'Log In'
        #         },
        #         callback=self.parse
        #     )
        # ]
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    @property
    def html_snippet(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title></title>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

    @staticmethod
    def filename(url):
        return list(filter(None, url.split("/")))[-1].split('?')[0]

    @staticmethod
    def save_parsed_images(selectors):
        for selector in selectors:
            attr = getattr(selector, 'attrib', {})
            src = attr.get('src')
            if src:
                path, filename = src.rsplit('/', 1)
                path = os.path.join(BASE_DIR, f'../templates{path}')
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(os.path.join(path, filename), 'wb') as f:
                    response = requests.get(
                        f'{BASE_URL}{src}', stream=True,
                        timeout=(3, 10), verify=True
                    )
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                time.sleep(1)

    @staticmethod
    def save_parsed_js(selectors):
        for selector in selectors:
            attr = getattr(selector, 'attrib', {})
            src = attr.get('src')
            if src:
                path, filename = src.rsplit('/', 1)
                path = os.path.join(BASE_DIR, f'../templates{path}')
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(os.path.join(path, filename), 'wb') as f:
                    response = requests.get(
                        f'{BASE_URL}{src}', timeout=(3, 10), verify=True
                    )
                    f.write(response.content)
                time.sleep(1)

    @staticmethod
    def save_parsed_css(selectors):
        for selector in selectors:
            attr = getattr(selector, 'attrib', {})
            src = attr.get('href')
            if src and '/' in src:
                path, filename = src.rsplit('/', 1)
                path = os.path.join(BASE_DIR, f'../templates{path}')
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(os.path.join(path, filename), 'wb') as f:
                    response = requests.get(
                        f'{BASE_URL}{src}', timeout=(3, 10), verify=True
                    )
                    f.write(response.content)
                time.sleep(1)

    def save(self, response):
        self.driver.get(response.request.url)
        wait = WebDriverWait(self.driver, 100)
        # self.save_parsed_js(response.xpath('//script'))
        # self.save_parsed_css(response.xpath('//link'))
        # self.save_parsed_images(response.xpath('//img'))
        filename = self.filename(response.url)
        path = os.path.join(BASE_DIR, f'../templates/{filename}.html')
        content = response.selector.xpath('//div[@id="topicContent"]').get()
        with open(path, 'wb') as f:
            # f.write(self.html_snippet.format(content=content))
            f.write(response.body)

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formid='loginForm',
            formname='loginForm',
            clickdata={'id': 'btnLoginSubmit'},
            formdata={
                'userName': USERNAME, 'password': PASSWORD,
                'saveUserName': 'true', 'isSubmitting': 'true',
                'loginText': 'Log In'
            },
            callback=self.after_login
        )
        # yield scrapy.http.JsonRequest(url=JSON_LOGIN_URL)
        # start_urls = [
        #     'https://www.uptodate.com/contents/overview-of-general-medical-care-'
        #     'in-nonpregnant-adults-with-diabetes-mellitus?search=diabetis&source'
        #     '=search_result&selectedTitle=1~150&usage_type=default&display_rank=1'
        #     '#H15053957'
        # ]
        # for url in start_urls:
        #     yield SeleniumRequest(url=url, callback=self.save)
        # yield None

    def after_login(self, response):
        # self.save(response)
        # for row in response.css('table.files tr'):
        #     item_link = row.css('td.content a').attrib.get('href')
        #
        #     if not item_link:
        #         yield None
        #     elif self.check_file(item_link):
        #         item_raw_link = self.get_raw_url(item_link)
        #         yield Request(item_raw_link, callback=self.parse_file)
        #     elif not '/blob/' in item_link:
        #         item_abs_link = self.get_abs_url(
        #             item_link,
        #             response.request.url
        #         )
        #         yield Request(item_abs_link, callback=self.parse)
        #
        # return self._parse_response(response, self.parse_start_url,
        #                             cb_kwargs={}, follow=True)
        start_urls = [
            # 'https://www.uptodate.com/contents/overview-of-general-medical-care-'
            # 'in-nonpregnant-adults-with-diabetes-mellitus?search=diabetis&source'
            # '=search_result&selectedTitle=1~150&usage_type=default&display_rank=1'
            # '#H15053957'
            'https://www.uptodate.com/contents/'
            'overview-of-general-medical-care-in-nonpregnant-'
            'adults-with-diabetes-mellitus'
        ]
        for url in start_urls:
            yield SeleniumRequest(url=url, callback=self.save)
        yield None
