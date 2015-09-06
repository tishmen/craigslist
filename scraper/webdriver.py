import logging
import os
import time
import random
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from django.conf import settings

log = logging.getLogger('craigslist')


class Webdriver(object):

    def __init__(self):
        self.page_load_timeout = 90
        self.implicitly_wait = 10
        self.min_sleep = 5
        self.max_sleep = 10
        self.stamp = datetime.now().isoformat()

    def start(self):
        self.webdriver = webdriver.PhantomJS(
            service_args=['--ssl-protocol=any']
        )
        self.webdriver.maximize_window()
        self.webdriver.set_page_load_timeout(self.page_load_timeout)
        self.webdriver.implicitly_wait(self.implicitly_wait)
        log.debug('started webdriver')

    def stop(self):
        self.webdriver.quit()
        log.debug('stoped webdriver')

    def sleep(self):
        seconds = random.uniform(self.min_sleep, self.max_sleep)
        log.debug('sleeping {} seconds'.format(seconds))
        time.sleep(seconds)

    def get(self, url):
        try:
            self.webdriver.get(url)
        except TimeoutException:
            body = self.element(By.TAG_NAME, 'body')
            self.send_keys(body, 'body', Keys.ESCAPE)
        log.debug('went to {}'.format(url))
        self.sleep()

    def send_keys(self, element, name, keys):
        element.send_keys(keys)
        log.debug('sent {} to {}'.format(keys, name))
        self.sleep()

    def click(self, element, name):
        element.click()
        log.debug('clicked {}'.format(name))
        self.sleep()

    def scroll(self, element, name):
        self.webdriver.execute_script(
            'return arguments[0].scrollIntoView();', element
        )
        log.debug('scrolled to {} element'.format(name))

    def element(self, by, selector, name):
        element = self.webdriver.find_element(by, selector)
        log.debug('found {} element'.format(name))
        return element

    def elements(self, by, selector, name):
        elements = self.webdriver.find_elements(by, selector)
        log.debug('found {} {} elements'.format(len(elements), name))
        return elements

    def random_element(self, elements):
        return random.choice(elements)
        log.debug(
            'choose random element from {} elements'.format(len(elements))
        )

    def screenshot(self):
        path = os.path.join(settings.ERROR_DIR, '{}.png'.format(self.stamp))
        self.webdriver.get_screenshot_as_file(path)
        log.debug('took screenshot as {}'.format(path))

    def source(self):
        path = os.path.join(settings.ERROR_DIR, '{}.html'.format(self.stamp))
        with open(path, 'w') as f:
            f.write(self.webdriver.page_source)
        log.debug('saved source as {}'.format(path))

    def onerror(self):
        self.screenshot()
        self.source()
