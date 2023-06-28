import inspect
import logging
import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup")
class BaseClass:

    def get_logger(self):
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)  # filehandler object

        logger.setLevel(logging.INFO)
        return logger

    def get_title(self, title):
        WebDriverWait(self.driver, 4).until(
            ec.title_is(title))
        return self.driver.title