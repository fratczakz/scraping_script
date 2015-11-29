import time
import logging


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


logger = logging.getLogger(__name__)


class O2Browser(webdriver.Firefox):
    url = """
http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk
"""
    search_bar_xpath = "//input[@id='countryName']"
    pay_monthly_xpath = "//a[@id='paymonthly']"
    element_xpath = (
        "//div[@id='propositionContainer']/div[2]"
        "//td[@id='landLine']/strong"
    )

    def query_country(self, query, wait=2):
        """Query the search for the country. It opens the page with rates for
        a country

        :param query: Country name
        :type query: str
        :param wait: Time to wait for page load.
        :type wait: int
        """

        self.get(self.url)
        elem = self.find_element_by_xpath(
            self.search_bar_xpath
        )
        elem.send_keys(query + Keys.RETURN)
        time.sleep(wait)

    def get_land_line_value(self, wait=2):
        """Parse the value out of the country page.

        :param wait: Time to wait for page load.
        :type wait: int
        :return: Value or None if not available.
        :rtype: int or None
        """

        try:
            el = self.find_element_by_xpath(self.pay_monthly_xpath)
            el.click()
            time.sleep(wait)
            el = self.find_element_by_xpath(self.element_xpath)
            return self.parse_land_line(
                el.text
            )
        except NoSuchElementException, e:
            logger.warn("Could not find an element: %s", e)
            return None

    def parse_land_line(self, value):
        """Handle the parsing of the string value to int.

        :param value: Parsed value as str.
        :type value: str
        :returns: Value as int.
        :rtype: int
        """

        return int(value.strip('p'))
