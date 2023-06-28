import pytest
import time
from selenium.webdriver.support.select import Select
from pageObjects.AttendancePage import AttendancePage
from pageObjects.HomePage import HomePage
from pageObjects.LoginPage import LoginPage
from utilities.BaseClass import BaseClass
from pageObjects.LeaveRequestsPage import LeaveRequestsPage


class TestApplyLeaveRequest(BaseClass):

    def test_login(self, data_hrms_id):
        log = self.get_logger()
        login_page = LoginPage(self.driver)
        log.info("HRMS Id is " + data_hrms_id)
        login_page.get_hrms_id().send_keys(data_hrms_id)
        log.info("Clicking on Generate OTP button")
        login_page.get_generate_otp().click()
        log.info("Verifying presence of OTP elements ")
        login_page.verify_otp_input_presence()
        log.info("Getting OTP elements")
        otp_elements = login_page.get_otp_input_elements()
        log.info("Entering the data ")
        for otp_element in otp_elements:
            login_page.get_input_element(otp_element).send_keys(0)
        log.info("Getting Login Button")
        login_page.get_login_button().click()
        login_page.handle_announcement_popup()
        title = self.get_title("Home")
        assert title == "Home"

    def test_home_page(self):
        log = self.get_logger()
        home_page = HomePage(self.driver)
        log.info("Getting Attendance Link element")
        home_page.get_attendance_element().click()
        log.info("Getting My Attendance Link element")
        home_page.get_my_attendance_element().click()
        title = self.get_title("My Attendance")
        assert title == "My Attendance"

    def test_attendance(self):
        attendance_page_handler = AttendancePage(self.driver)
        payroll_element = attendance_page_handler.get_payroll_dropdown_element()
        payroll_dropdown_element = Select(payroll_element)
        payroll_dropdown_element.select_by_value("PAST_CYCLE")
        time.sleep(2)
        attendance_table_element = attendance_page_handler.get_attendance_table_element()
        table_cols = attendance_page_handler.get_table_cols(attendance_table_element)
        absent_details: list = []
        for table_col in table_cols:
            table_rows_in_col = attendance_page_handler.get_table_row_in_col(table_col)
            for table_row in table_rows_in_col:
                if (attendance_page_handler.get_first_half(table_row) == "A" and
                        attendance_page_handler.get_second_half(table_row) == "A"):
                    absent_date = attendance_page_handler.get_absent_date(table_row)
                    absent_details.append((absent_date, "Full Day"))
                    break
                elif (attendance_page_handler.get_first_half(table_row) == "A" and
                        attendance_page_handler.get_second_half(table_row) != "A"):
                    absent_date = attendance_page_handler.get_absent_date(table_row)
                    absent_details.append((absent_date, "First Half"))
                    break
                elif (attendance_page_handler.get_first_half(table_row) != "A" and
                        attendance_page_handler.get_second_half(table_row) == "A"):
                    absent_date = attendance_page_handler.get_absent_date(table_row)
                    absent_details.append((absent_date, "Second Half"))
                    break
            if len(absent_details) == 0:
                continue
            else:
                break
        print(absent_details)
        attendance_page_handler.get_my_leaves_element().click()
        attendance_page_handler.get_leaves_element().click()
        attendance_page_handler.get_apply_leave_button_element().click()
        apply_leave_modal = attendance_page_handler.get_apply_leave_modal_element()
        leave_types_row_element = attendance_page_handler.get_leave_types_row_element(apply_leave_modal)
        leave_types_with_count = attendance_page_handler.get_leave_types_with_count_element(leave_types_row_element)
        possible_choices_list = attendance_page_handler.get_selected_leave_type_element(
                                                        leave_types_with_count, absent_details)
        possible_choices_list[0].click()
        attendance_page_handler.get_from_date_picker_element().click()
        attendance_page_handler.get_required_absent_date_element(absent_details[0][0]).click()
        if absent_details[0][1] == "First Half" or absent_details[0][1] == "Second Half":
            attendance_page_handler.get_leave_mode_element().click()
            attendance_page_handler.get_leave_mode_type(absent_details[0][1])
        attendance_page_handler.get_to_date_picker_element().click()
        attendance_page_handler.get_required_absent_date_element(absent_details[0][0]).click()
        attendance_page_handler.get_purpose_of_leave_text_element().send_keys("Test Purpose DATA")
        attendance_page_handler.get_submit_btn_element().click()
        time.sleep(1)

    def test_reporting_manager_login(self):
        home_page = HomePage(self.driver)
        home_page.get_home_element().click()
        home_page.get_dashboard_element().click()
        reporting_manager_id = home_page.get_reporting_manager_hrms_id()
        home_page.get_profile_link_element().click()
        home_page.logout_element().click()
        login_page = LoginPage(self.driver)
        login_page.get_hrms_id().send_keys(reporting_manager_id)
        login_page.get_generate_otp().click()
        login_page.verify_otp_input_presence()
        otp_elements = login_page.get_otp_input_elements()
        for otp_element in otp_elements:
            login_page.get_input_element(otp_element).send_keys(0)
        login_page.get_login_button().click()
        login_page.handle_announcement_popup()
        title = self.get_title("Home")
        assert title == "Home"

    def test_approve_leave_request(self):
        leave_requests = LeaveRequestsPage(self.driver)
        leave_requests.get_my_team_locator().click()
        leave_requests.get_leave_requests_element_locator().click()
        leave_requests.get_approve_button_element().click()
        modal = leave_requests.get_approval_modal_element()
        leave_requests.get_text_area_button_element(modal).send_keys("Test Approval Leave Request")
        time.sleep(2)
        leave_requests.get_final_approval_button_element().click()
        time.sleep(1)
        leave_requests.get_profile_link_element().click()
        leave_requests.get_logout_element().click()

    @pytest.fixture()
    def data_hrms_id(self):
        return "MED1067524"
