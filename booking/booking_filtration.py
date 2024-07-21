# This file will include a class with instance methods.
# That will be responsible to interact with our website
# After we have some results, to apply filtration.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        for star in star_values:
            while True:
                try:
                    # Locate the input element based on the aria-label containing the star value
                    star_rating_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f"//input[contains(@aria-label, '{star} stars')]"))
                    )

                    # Click on the parent element
                    star_rating_input.click()

                    # Wait for the page to reload completely
                    # by waiting for an element that indicates the page has reloaded
                    WebDriverWait(self.driver, 10).until(
                        EC.staleness_of(star_rating_input)
                    )

                    # Ensure that the next star rating is only clicked after the page has reloaded
                    break
                except StaleElementReferenceException:
                    print("StaleElementReferenceException caught, retrying...")

                except Exception as e:
                    break

    def sort_price_lowest_first(self):
        sorting_dropdown = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='sorters-dropdown-trigger']")
        sorting_dropdown.click()
        self.driver.find_element(By.CSS_SELECTOR, "button[data-id='price']").click()
