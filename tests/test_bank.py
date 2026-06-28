import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

class TestBank:

    @pytest.fixture
    def driver(self):
        # Просто создаем драйвер без всяких опций
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/?balance=30000&reserved=20001')
        yield driver
        driver.quit()

    def handle_alert(self, driver):
        try:
            alert = driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except NoAlertPresentException:
            return None

    def test_negative_amount_not_allowed(self, driver):
        wait = WebDriverWait(driver, 10)
        
        rub_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'Рубл')]")
        rub_tab.click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
        card_input = driver.find_element(By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
        card_input.clear()
        card_input.send_keys('9344 5524 5665 3667')
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']")))
        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys('-100')
        
        button = driver.find_element(By.CSS_SELECTOR, "button.g-button")
        button.click()
        
        wait.until(EC.alert_is_present())
        alert_text = self.handle_alert(driver)
        
        assert alert_text is not None
        assert 'принят банком' not in alert_text, f'Отрицательная сумма не должна приниматься! Текст: {alert_text}'

    def test_zero_amount_not_allowed(self, driver):
        wait = WebDriverWait(driver, 10)
        
        rub_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'Рубл')]")
        rub_tab.click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
        card_input = driver.find_element(By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
        card_input.clear()
        card_input.send_keys('9344 5524 5665 3667')
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']")))
        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys('0')
        
        button = driver.find_element(By.CSS_SELECTOR, "button.g-button")
        button.click()
        
        wait.until(EC.alert_is_present())
        alert_text = self.handle_alert(driver)
        
        assert alert_text is not None
        assert 'принят банком' not in alert_text, f'Нулевая сумма не должна приниматься! Текст: {alert_text}'

    def test_transfer_more_than_balance_usd(self, driver):
        wait = WebDriverWait(driver, 10)
        
        usd_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'Доллар')]")
        usd_tab.click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
        card_input = driver.find_element(By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
        card_input.clear()
        card_input.send_keys('9344 5524 5665 3667')
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']")))
        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys('1500')
        
        button = driver.find_element(By.CSS_SELECTOR, "button.g-button")
        button.click()
        
        wait.until(EC.alert_is_present())
        alert_text = self.handle_alert(driver)
        
        assert alert_text is not None
        assert 'принят банком' not in alert_text, f'Перевод больше баланса не должен приниматься! Текст: {alert_text}'

    def test_commission_wrong(self, driver):
        """BUG-003: комиссия для 150 ₽ должна быть 15 ₽, а не 10 ₽"""
        wait = WebDriverWait(driver, 10)
        
        rub_tab = driver.find_element(By.XPATH, "//*[contains(text(), 'Рубл')]")
        rub_tab.click()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")))
        card_input = driver.find_element(By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
        card_input.clear()
        card_input.send_keys('9344 5524 5665 3667')
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']")))
        amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys('150')
        
        commission_text = driver.find_element(By.XPATH, "//*[contains(text(), 'Комиссия')]").text
        assert 'Комиссия: 15' in commission_text, f'Баг! Комиссия должна быть 15, а не 10! Текст: {commission_text}'
