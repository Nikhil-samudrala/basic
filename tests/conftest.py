import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    driver.get("https://hrmstest.medplusindia.com/login")
    driver.maximize_window()

    driver.implicitly_wait(1)
    request.cls.driver = driver
    yield
    driver.close()
