# This file is going to include method that will parse
# The specific data that we need from each of the deal boxes
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        # Targeting the div which has the complete list of hotels
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")

    def pull_hotel_attributes(self):
        # List to store the result
        collection = []
        count = 0
        for deal_box in self.deal_boxes:
            # Pulling the hotel name
            hotel_name = deal_box.find_element(By.CSS_SELECTOR, ".e037993315.f5f8fe25fa").get_attribute(
                'innerHTML').strip()

            # Pulling the hotel price
            hotel_price = deal_box.find_element(By.CSS_SELECTOR, ".e037993315.ab91cb3011.d9315e4fb0").get_attribute(
                'innerHTML').strip()
            hotel_price = hotel_price.replace("&nbsp;", "")

            # Pulling the hotel rating
            rating = (By.CSS_SELECTOR, ".d0522b0cca.fd44f541d8")
            try:
                hotel_rating = WebDriverWait(deal_box, 10).until(
                    EC.visibility_of_element_located(rating)).get_attribute('textContent').strip()
            except TimeoutException:
                hotel_rating = ' '

            # Regex to filter the rating from complete string
            pattern = r'\b\d+(\.\d+)?\b'
            hotel_rating = re.search(pattern, hotel_rating)

            # Accept results which have missing ratings
            try:
                hotel_rating = hotel_rating.group()
            except AttributeError:
                hotel_rating = ' '

            # Count for the S.No. of the hotel
            count += 1

            # Adding the hotel to the list
            collection.append([count, hotel_name, hotel_price, hotel_rating])

        return collection
