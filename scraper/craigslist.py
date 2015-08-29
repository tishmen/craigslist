import logging
import random

from selenium.webdriver.common.by import By

from scraper.webdriver import Webdriver

log = logging.getLogger('craigslist')


class CraigslistScraper(Webdriver):

    def get_id(self):
        url = self.webdriver.current_url
        return int(url.split('/')[-1].split('.html')[0])

    def get_email(self):
        email = self.element(By.CLASS_NAME, 'anonemail', 'email text')
        return email.text

    def scrape(self, scraper):
        try:
            log.debug('starting {} scraper'.format(scraper.name))
            self.start()
            self.webdriver.get('https://accounts.craigslist.org/login/home')

            email = self.element(By.ID, 'inputEmailHandle', 'email input')
            self.send_keys(email, 'email input', scraper.email)

            password = self.element(By.ID, 'inputPassword', 'password input')
            self.send_keys(password, 'password input', scraper.password)

            login = self.element(By.TAG_NAME, 'button', 'login button')
            self.click(login, 'login button')

            home = self.element(By.CSS_SELECTOR, '.bchead > a', 'home link')
            self.click(home, 'home link')

            housing = self.element(By.CLASS_NAME, 'apa', 'housing link')
            self.click(housing, 'housing link')

            min_price = self.element(
                By.CSS_SELECTOR, '.flatinput.min', 'minimum price input'
            )
            self.send_keys(min_price, 'minimum price input', scraper.min_price)

            max_price = self.element(
                By.CSS_SELECTOR, '.flatinput.max', 'maximum price input'
            )
            self.send_keys(max_price, 'maximum price input', scraper.max_price)

            bedrooms = self.element(
                By.CSS_SELECTOR,
                'option[value="{}"]'.format(scraper.bedroom_count),
                'bedrooms select'
            )
            self.click(bedrooms, 'bedrooms select')

            results = []
            postings = self.elements(By.CLASS_NAME, 'hdrlnk', 'postings link')
            random.shuffle(postings)
            count = random.randint(scraper.min_postings, scraper.max_postings)
            for i, posting in enumerate(postings[:count]):
                self.scroll(posting, '{} posting'.format(i))
                self.click(posting, '{} posting'.format(i))

                reply = self.element(
                    By.CLASS_NAME, 'reply_button', 'reply button'
                )
                self.click(reply, 'reply button')

                email = self.get_email()
                if not email:
                    continue
                results.append({'email': email, 'id': self.get_id()})

            log.debug('got {} results'.format(len(results)))
            return results
        except Exception:
            self.onerror()
            raise
        finally:
            self.stop()
            log.debug('stoped {} scraper'.format(scraper.name))
