from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    hrms_id = (By.CSS_SELECTOR, "input[name='username']")
    generate_otp = (By.CSS_SELECTOR, "button[type='submit']")
    otp_input_elements = (By.CSS_SELECTOR, "div[style='display: flex; align-items: center;']" )
    input_element = (By.CSS_SELECTOR, "input")
    login_button = (By.CSS_SELECTOR, "button[type='submit']")
    close_button_selector = (By.CSS_SELECTOR, "button[class='close']")

    def get_hrms_id(self):
        return self.driver.find_element(*LoginPage.hrms_id)

    def get_generate_otp(self):
        return self.driver.find_element(*LoginPage.generate_otp)

    def verify_otp_input_presence(self):
        element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "(//div[contains(@class,'form-group')])[2]")))

    def get_otp_input_elements(self):
        return self.driver.find_elements(*LoginPage.otp_input_elements)

    def get_input_element(self, otp_element):
        return otp_element.find_element(*LoginPage.input_element)

    def get_login_button(self):
        return self.driver.find_element(*LoginPage.login_button)

    def handle_announcement_popup(self):
        # try:
        #     wait = WebDriverWait(self.driver, 5)
        #     announcement = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "modal custom-modal fade show")))
        #     announcement.find_element(*LoginPage.close_button_selector).click()
        # except TimeoutException:
        #     return

        wait = WebDriverWait(self.driver, 5)
        announcement = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "div[class='modal custom-modal fade show']")))
        announcement.find_element(*LoginPage.close_button_selector).click()
        return




