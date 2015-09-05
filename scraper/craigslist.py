import logging
import random

from selenium.webdriver.common.by import By

from scraper.webdriver import Webdriver

log = logging.getLogger('craigslist')


class CraigslistScraper(Webdriver):

    def get_url(self):
        return self.webdriver.current_url

    def get_email(self):
        try:
            email = self.element(By.CLASS_NAME, 'anonemail', 'email text')
            return email.text
        except Exception:
            log.error('unable to find email')
            return None

    def scrape(
            self, name, email, password, city, min_price, max_price,
            bedroom_count, posting_count):
        try:
            log.debug('starting {} scraper'.format(name))
            self.start()
            self.get('https://accounts.craigslist.org/login/home')

            email_input = self.element(
                By.ID, 'inputEmailHandle', 'email input'
            )
            self.send_keys(email_input, 'email input', email)

            password_input = self.element(
                By.ID, 'inputPassword', 'password input'
            )
            self.send_keys(password_input, 'password input', password)

            login_button = self.element(By.TAG_NAME, 'button', 'login button')
            self.click(login_button, 'login button')

            self.get('http://{}.craigslist.org/search/apa'.format(city))

            min_price_input = self.element(
                By.CSS_SELECTOR, '.flatinput.min', 'minimum price input'
            )
            self.send_keys(min_price_input, 'minimum price input', min_price)

            max_price_input = self.element(
                By.CSS_SELECTOR, '.flatinput.max', 'maximum price input'
            )
            self.send_keys(max_price_input, 'maximum price input', max_price)

            bedrooms_select = self.element(
                By.CSS_SELECTOR,
                'option[value="{}"]'.format(bedroom_count),
                'bedrooms select'
            )
            self.click(bedrooms_select, 'bedrooms select')

            results = []
            posting_links = self.elements(
                By.CLASS_NAME, 'hdrlnk', 'posting links'
            )
            urls = [link.get_attribute('href') for link in posting_links]
            random.shuffle(urls)
            for url in urls[:posting_count]:
                self.get(url)
                reply_button = self.element(
                    By.CLASS_NAME, 'reply_button', 'reply button'
                )
                self.click(reply_button, 'reply button')

                email = self.get_email()
                if not email:
                    break
                results.append({'url': self.get_url(), 'email': email})

            log.debug('got {} results'.format(len(results)))
            return results
        except Exception:
            self.onerror()
            raise
        finally:
            self.stop()
            log.debug('stoped {} scraper'.format(name))
