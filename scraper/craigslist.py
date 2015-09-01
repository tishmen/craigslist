import logging
import random

from selenium.webdriver.common.by import By

from scraper.webdriver import Webdriver

log = logging.getLogger('craigslist')


class CraigslistScraper(Webdriver):

    def get_url(self):
        return self.webdriver.current_url

    def get_id(self):
        url = self.webdriver.current_url
        return int(url.split('/')[-1].split('.html')[0])

    def get_email(self):
        email = self.element(By.CLASS_NAME, 'anonemail', 'email text')
        return email.text

    def scrape(
            self, name, email, password, min_price, max_price, bedroom_count,
            posting_count):
        try:
            log.debug('starting {} scraper'.format(name))
            self.start()
            self.webdriver.get('https://accounts.craigslist.org/login/home')

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

            home_link = self.element(
                By.CSS_SELECTOR, '.bchead > a', 'home link'
            )
            self.click(home_link, 'home link')

            housing_link = self.element(
                By.CLASS_NAME, 'apa', 'housing link'
            )
            self.click(housing_link, 'housing link')

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
            random.shuffle(posting_links)
            for i, posting_link in enumerate(
                    posting_links[:posting_count]):
                self.scroll(posting_link, '{} posting link'.format(i))
                self.click(posting_link, '{} posting_link'.format(i))

                reply_button = self.element(
                    By.CLASS_NAME, 'reply_button', 'reply button'
                )
                self.click(reply_button, 'reply button')

                email = self.get_email()
                if not email:
                    continue
                results.append(
                    {
                        'id': self.get_id(),
                        'url': self.get_url(),
                        'email': email,
                    }
                )

            log.debug('got {} results'.format(len(results)))
            return results
        except Exception:
            self.onerror()
            raise
        finally:
            self.stop()
            log.debug('stoped {} scraper'.format(name))
