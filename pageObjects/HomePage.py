from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    attendance_locator = (By.LINK_TEXT, "Attendance")
    my_attendance_element_locator = (By.LINK_TEXT, "My Attendance")
    home_element_locator = (By.LINK_TEXT, "Home")
    reporting_manager_locator = (By.CSS_SELECTOR, "div[class='profile-info-left'] div[class='staff-id']")
    dashboard_element_locator = (By.LINK_TEXT, "Dashboard")
    profile_link_locator = (By.CSS_SELECTOR, "a[class='dropdown-toggle nav-link']")
    logout_locator = (By.LINK_TEXT, "Logout")

    def get_attendance_element(self):
        return self.driver.find_element(*HomePage.attendance_locator)

    def get_my_attendance_element(self):
        return self.driver.find_element(*HomePage.my_attendance_element_locator)

    def get_home_element(self):
        return self.driver.find_element(*HomePage.home_element_locator)

    def get_dashboard_element(self):
        return self.driver.find_element(*HomePage.dashboard_element_locator)

    def get_reporting_manager_hrms_id(self):
        return self.driver.find_elements(*HomePage.reporting_manager_locator)[-1].text.split('(')[1].split(')')[0]

    def get_profile_link_element(self):
        return self.driver.find_element(*HomePage.profile_link_locator)

    def logout_element(self):
        return self.driver.find_element(*HomePage.logout_locator)


