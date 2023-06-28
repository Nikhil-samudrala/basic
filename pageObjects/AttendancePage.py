from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import datetime


def get_required_date_picker_format(absent_date):
    day, month = absent_date.split(' ')[0].split('/')
    year = datetime.date.today().year
    date_picker_format = str(year) + '-' + month + '-' + day
    return date_picker_format


class AttendancePage:

    def __init__(self, driver):
        self.driver = driver

    table_cols_locator = (By.CSS_SELECTOR, "div[class='col-lg-4 col-md-6']")
    table_row_locator = (By.CSS_SELECTOR, "tr[class='ant-table-row ant-table-row-level-0']")
    date_locator = (By.TAG_NAME, "h2")
    full_day_locator = (By.CSS_SELECTOR, "span[class*='attendance-buttons'")
    my_leaves_locator = (By.LINK_TEXT, "Leaves")
    leaves_locator = (By.LINK_TEXT, "My Leaves")
    apply_leave_button_locator = (
        By.CSS_SELECTOR, "div[class='page-header'] button[class='btn btn-primary submit-btn']")
    apply_leave_modal_locator = (By.ID, "apply_leave")
    leave_types_row_locator = (By.CLASS_NAME, "row")
    leave_type_text_locator = (By.TAG_NAME, "label")
    radio_button_locator = (By.TAG_NAME, "input")
    count_locator = (By.TAG_NAME, "span")
    from_date_picker_locator = (By.NAME, "fromDate")
    leave_mode_element_locator = (By.CSS_SELECTOR, "span[title='Full Day']")
    leave_mode_types_locator = (By.CSS_SELECTOR, "div[class='ant-select-item-option-content']")
    to_date_picker_locator = (By.NAME, "toDate")
    date_picker_table_active_elements_locator = (By.CSS_SELECTOR, "td[class*='ant-picker-cell-in-view']")
    purpose_of_leave_text_locator = (By.NAME, "purpose")
    submit_btn_locator = (By.CSS_SELECTOR, "button[class='btn btn-primary submit-btn']")
    payroll_dropdown_locator = (By.CSS_SELECTOR, "select[class=' form-control floating']")
    diagonal_attendance_locator = (By.CSS_SELECTOR, "span[class='left-name']")

    def get_attendance_table_element(self):
        return WebDriverWait(self.driver, 5).until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "div[class='tab-content'] div[class='row']")))

    def get_payroll_dropdown_element(self):
        return self.driver.find_element(*AttendancePage.payroll_dropdown_locator)

    def get_table_cols(self, attendance_table):
        return attendance_table.find_elements(*AttendancePage.table_cols_locator)

    def get_table_row_in_col(self, table_col):
        return table_col.find_elements(*AttendancePage.table_row_locator)

    def get_first_half(self, table_row):
        try:
            return table_row.find_elements(*AttendancePage.full_day_locator)[0].text
        except:
            return table_row.find_elements(*AttendancePage.diagonal_attendance_locator)[0].text

    def get_second_half(self, table_row):
        try:
            return table_row.find_elements(*AttendancePage.full_day_locator)[1].text
        except:
            return table_row.find_elements(*AttendancePage.diagonal_attendance_locator)[1].text

    def get_absent_date(self, table_row):
        return table_row.find_element(*AttendancePage.date_locator).accessible_name

    def get_my_leaves_element(self):
        return self.driver.find_element(*AttendancePage.my_leaves_locator)

    def get_leaves_element(self):
        return self.driver.find_element(*AttendancePage.leaves_locator)

    def get_apply_leave_button_element(self):
        return self.driver.find_element(*AttendancePage.apply_leave_button_locator)

    def get_apply_leave_modal_element(self):
        wait = WebDriverWait(self.driver, 2)
        return wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "div[class='modal custom-modal fade show']")))

    def get_leave_types_row_element(self, modal):
        return modal.find_elements(*AttendancePage.leave_types_row_locator)[1]

    def get_leave_types_with_count_element(self, leave_types_row_element):
        leave_types_elements = leave_types_row_element.find_elements(By.CLASS_NAME, "card-body")
        leaves_types_info = []
        for leave_types_element in leave_types_elements:
            leave_type = leave_types_element.find_element(*AttendancePage.leave_type_text_locator).text
            radio_button = leave_types_element.find_element(*AttendancePage.radio_button_locator)
            try:
                count = leave_types_element.find_element(*AttendancePage.count_locator).text
            except NoSuchElementException:
                count = None
            leaves_types_info.append((leave_type, radio_button, count))
        print(leaves_types_info)

        return leaves_types_info

    def get_selected_leave_type_element(self, leave_types_with_count, absent_details):
        absent_type = absent_details[0][1]
        possible_choices = []
        for leave_type_with_count in leave_types_with_count[0:-1]:
            if absent_type == "Full Day" and \
                    (leave_type_with_count[0].split(" ")[0] == "OPTIONAL"
                     and float(leave_type_with_count[2].split('(')[1][0:-1]) >= 1):
                possible_choices.append(leave_type_with_count[1])
                continue
            elif (float(leave_type_with_count[2].split('(')[1][0:-1]) > 0.5 and absent_type == "Full Day" and
                  leave_type_with_count[0].split(" ")[0] != "OPTIONAL"):
                possible_choices.append(leave_type_with_count[1])
            elif (float(leave_type_with_count[2].split('(')[1][0:-1]) >= 0.5 and
                  (absent_type == "First Half" or absent_type == "Second Half") and
                  leave_type_with_count[0].split(" ")[0] != "OPTIONAL"):
                possible_choices.append(leave_type_with_count[1])
        if len(possible_choices) > 0:
            return possible_choices
        else:
            possible_choices.append(leave_types_with_count[-1][1])
            return possible_choices

    def get_from_date_picker_element(self):
        return self.driver.find_element(*AttendancePage.from_date_picker_locator)

    def get_to_date_picker_element(self):
        return self.driver.find_element(*AttendancePage.to_date_picker_locator)

    def get_leave_mode_element(self):
        return self.driver.find_element(*AttendancePage.leave_mode_element_locator)

    def get_leave_mode_type(self, leave_mode):
        self.driver.find_element(By.CSS_SELECTOR, f"div[title='{leave_mode}']").click()

    def get_required_absent_date_element_helper(self, absent_date):
        date_picker_format = get_required_date_picker_format(absent_date)
        active_elements = self.driver.find_elements(*AttendancePage.date_picker_table_active_elements_locator)
        if len(active_elements) > 31:
            active_elements = active_elements[int(len(active_elements) / 2): int(len(active_elements)) - 1]
        for active_element in active_elements:
            if active_element.get_attribute('title') == date_picker_format:
                return active_element

    def get_required_absent_date_element(self, absent_date):
        required_element = AttendancePage(self.driver).get_required_absent_date_element_helper(absent_date)
        if not required_element:
            self.driver.find_element(By.CSS_SELECTOR, 'button[class="ant-picker-header-prev-btn"]').click()
            return AttendancePage(self.driver).get_required_absent_date_element_helper(absent_date)
        return required_element

    def get_submit_btn_element(self):
        return self.driver.find_elements(*AttendancePage.submit_btn_locator)[1]

    def get_purpose_of_leave_text_element(self):
        return self.driver.find_element(*AttendancePage.purpose_of_leave_text_locator)
