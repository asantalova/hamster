from selenium.webdriver.common.by import By

class ExploraHomePage:
    HOME_URL = 'https://explorajourneys.com/'
    DESTINATION_FIELD = (By.CSS_SELECTOR, '.quickBooking__destination')
    DESTINATION_LIST = (By.CSS_SELECTOR, '.quickBooking__place')

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.HOME_URL)

    def click_on_destination_field(self):
        element = self.driver.find_element(*self.DESTINATION_FIELD)
        self.driver.execute_script("arguments[0].click();", element)
    
    def get_destination_list(self):
        return self.driver.find_elements(*self.DESTINATION_LIST)
    
    def title(self):
        return self.driver.title

