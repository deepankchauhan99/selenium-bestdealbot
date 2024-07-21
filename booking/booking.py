import booking.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from booking.booking_filtration import BookingFiltration
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from booking.booking_report import BookingReport
from prettytable import PrettyTable
from selenium.common.exceptions import TimeoutException


class Booking(webdriver.Chrome):
    # def __init__(self, driver_path=r"C:\SeleniumDrivers"):

    def __init__(self, teardown=False):
        # self.driver_path = driver_path
        self.teardown = teardown
        options = Options()

        # Stops the window from closing after the automation is completed
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def close_popup(self, retries=3):
        for _ in range(2):
            try:
                popup = (By.CSS_SELECTOR, "button[aria-label='Dismiss sign-in info.'")
                print('Looking for Pop-ups')
                WebDriverWait(self, 2).until(EC.element_to_be_clickable(popup)).click()
                print("Pop-up closed")
                break

            except TimeoutException:
                print("No pop-ups found")
                continue

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        button = self.find_element(By.CSS_SELECTOR, "button[data-testid='header-currency-picker-trigger']")
        button.click()
        selected_currency = self.find_element(By.XPATH,
                                              f"//button[@data-testid='selection-item']//div[contains(text(), '{currency}')]")
        print(f"Currency Selected: {currency}")
        selected_currency.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, ':rh:')
        search_field.clear()
        search_field.send_keys(place_to_go)
        WebDriverWait(self, 10).until(EC.text_to_be_present_in_element((By.ID, "autocomplete-result-0"), place_to_go))
        first_result = self.find_element(By.ID, "autocomplete-result-0")
        first_result.click()
        print(f"Location selected: {place_to_go}")

    def select_dates(self, check_in_date, check_out_date):
        self.find_element(By.CSS_SELECTOR, f"span[data-date='{check_in_date}']").click()
        self.find_element(By.CSS_SELECTOR, f"span[data-date='{check_out_date}']").click()
        print(f"Dates selected: {check_in_date} to {check_out_date}")

    def select_persons(self, adults, children, rooms):
        self.find_element(By.CSS_SELECTOR, "button[data-testid='occupancy-config']").click()

        # Reset adult counter
        while True:
            adults_element = self.find_element(By.XPATH, "//*[@id=':ri:']/div/div[1]/div[2]/button[@tabindex='-1']")
            adults_element.click()
            adults_count_element = self.find_element(By.ID, "group_adults")
            adults_count = adults_count_element.get_attribute('value')
            children_element = self.find_element(By.XPATH, "//*[@id=':ri:']/div/div[2]/div[2]/button[@tabindex='-1']")
            children_element.click()
            children_count_element = self.find_element(By.ID, "group_children")
            children_count = children_count_element.get_attribute('value')
            try:
                rooms_element = self.find_element(By.XPATH, "//*[@id=':ri:']/div/div[3]/div[2]/button[@tabindex='-1']")
            except:
                rooms_element = self.find_element(By.XPATH, "//*[@id=':ri:']/div/div[5]/div[2]/button[@tabindex='-1']")
            rooms_element.click()
            rooms_count_element = self.find_element(By.ID, "no_rooms")
            rooms_count = rooms_count_element.get_attribute('value')
            if int(adults_count) == 1 and int(children_count) == 0 and int(rooms_count) == 1:
                break

        for _ in range(adults - 1):
            adults_element = self.find_element(By.XPATH, "//*[@id=':ri:']/div/div[1]/div[2]/button[2][@tabindex='-1']")
            adults_element.click()

        for _ in range(rooms - 1):
            rooms_element = self.find_element(By.XPATH, "//*[@id=':ri:']/div/div[3]/div[2]/button[2][@tabindex='-1']")
            rooms_element.click()

        if children:
            for _ in children:
                children_element = self.find_element(By.XPATH,
                                                     "//*[@id=':ri:']/div/div[2]/div[2]/button[2][@tabindex='-1']")
                children_element.click()

            for i, age in children.items():
                tab_open = self.find_element(By.CSS_SELECTOR, "button[data-testid='occupancy-config']").get_attribute(
                    'aria-expanded')
                if str(tab_open) == 'false':
                    self.find_element(By.CSS_SELECTOR, "button[data-testid='occupancy-config']").click()
                age_selector_element = self.find_element(By.XPATH,
                                                         f"//div[@data-testid='kids-ages']/div[{int(i)}]/div/select["
                                                         f"@name='age']")
                Select(age_selector_element).select_by_value(f"{age}")

        self.find_element(By.XPATH, f"//button[@type='submit']").click()
        print(f"Persons selected: {adults} adult(s), {(lambda c: 0 if c == 0 else len(c))(children)} children")
        print(f"Rooms selected: {rooms}")

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(*const.STARS)
        filtration.sort_price_lowest_first()
        print(f"Filters selected: Star Rating: {str(const.STARS)[1:-1]}")
        print(f"Filters selected: Sort: Lowest price first")

    def report_results(self):
        hotels = (By.CSS_SELECTOR, ".d830fa48ad.db402c28f2")
        hotel_boxes = WebDriverWait(self, 10).until(EC.visibility_of_element_located(hotels))
        print("Hotels found!")
        report = BookingReport(hotel_boxes)
        table = PrettyTable(field_names=['S.No.', 'Hotel Name', 'Hotel Price', 'Hotel Score'])
        print("Loading List...")
        table.add_rows(report.pull_hotel_attributes())
        print(table)
