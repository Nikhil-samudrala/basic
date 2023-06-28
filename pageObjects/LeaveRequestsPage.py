from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LeaveRequestsPage:

    def __init__(self, driver):
        self.driver = driver

    my_team_locator = (By.LINK_TEXT, "My Team")
    leave_requests_element_locator = (By.LINK_TEXT, "Leave Requests")
    profile_link_locator = (By.CSS_SELECTOR, "li[class='nav-item dropdown has-arrow main-drop']")
    logout_locator = (By.LINK_TEXT, "Logout")
    all_leave_requests_locator = (By.CSS_SELECTOR, "tr[class*='ant-table-row ant-table-row-level-0']")
    leave_request_info = (By.CSS_SELECTOR, " td[class='ant-table-cell']")
    team_member_name = (By.TAG_NAME, "span")
    approve_button_locator = (By.CSS_SELECTOR, "button[class*='btn-success']")
    final_approval_button_locator = (By.CSS_SELECTOR, "button[class='btn btn-primary submit-btn']")
    def get_my_team_locator(self):
        return self.driver.find_element(*LeaveRequestsPage.my_team_locator)

    def get_leave_requests_element_locator(self):
        return self.driver.find_element(*LeaveRequestsPage.leave_requests_element_locator)

    def get_approve_button_element(self):
        leave_requests = self.driver.find_elements(*LeaveRequestsPage.all_leave_requests_locator)
        for leave_request in leave_requests:
            request_info_cols = leave_request.find_elements(*LeaveRequestsPage.leave_request_info)
            team_member_name = request_info_cols[0].find_element(*LeaveRequestsPage.team_member_name).text
            if team_member_name == "MED1067524":
                return request_info_cols[-1].find_element(*LeaveRequestsPage.approve_button_locator)

    def get_profile_link_element(self):
        wait = WebDriverWait(self.driver, 4)
        return wait.until(ec.element_to_be_clickable(
            (By.CSS_SELECTOR, "li[class='nav-item dropdown has-arrow main-drop']")))
        # self.driver.find_element(*LeaveRequestsPage.profile_link_locator)

    def get_logout_element(self):
        return self.driver.find_element(*LeaveRequestsPage.logout_locator)

    def get_text_area_button_element(self, modal):
        return modal.find_element(By.TAG_NAME, "textarea")

    def get_approval_modal_element(self):
        wait = WebDriverWait(self.driver, 2)
        return wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "div[class='modal custom-modal fade show']")))

    def get_final_approval_button_element(self):
        return self.driver.find_elements(*LeaveRequestsPage.final_approval_button_locator)[1]


