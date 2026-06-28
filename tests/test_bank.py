import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestBank:
    
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome()
        driver.get('http://localhost:8000/?balance=30000&reserved=20001')
        yield driver
        driver.quit()
    
    def test_negative_amount_not_allowed(self, driver):
        """BUG-001: отрицательная сумма не должна приниматься"""
        amount = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        amount.clear()
        amount.send_keys('-100')
        
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit.click()
        
        page = driver.page_source
        assert 'принят банком' not in page
    
    def test_zero_amount_not_allowed(self, driver):
        """BUG-001: 0 не должен приниматься"""
        amount = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        amount.clear()
        amount.send_keys('0')
        
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit.click()
        
        page = driver.page_source
        assert 'принят банком' not in page
    
    def test_transfer_more_than_balance_usd(self, driver):
        """BUG-002: перевод больше баланса (доллары)"""
        usd = driver.find_element(By.XPATH, "//*[contains(text(), 'Доллары')]")
        usd.click()
        
        amount = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        amount.clear()
        amount.send_keys('1500')
        
        submit = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit.click()
        
        page = driver.page_source
        assert 'принят банком' not in page
    
    def test_commission_wrong(self, driver):
        """BUG-003: комиссия для 150 ₽ должна быть 15 ₽"""
        amount = driver.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        amount.clear()
        amount.send_keys('150')
        
        # Проверяем, что комиссия = 10, а должна быть 15
        commission = driver.find_element(By.XPATH, "//*[contains(text(), 'Комиссия')]/following-sibling::*")
        assert '15' in commission.text or '10' not in commission.text
