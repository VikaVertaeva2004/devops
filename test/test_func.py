from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
import time 


 
def open_page(driver):
    try:
        span_element = driver.find_element(By.XPATH, "//span[@class='mb-3 mb-md-0 text-body-secondary']")
        if span_element.text == "© 2024 Вертаева Виктория 221-351":
            return True
            print(Fore.GREEN, "\rСтраница успешно открылась", Style.RESET_ALL, Fore.CYAN)
        else:
            print(Fore.RED,"ERROR:", Style.RESET_ALL, "Во время открытия страницы произошла ошибка!", sep='')
            return False
    except:
        print(Fore.RED,"ERROR:", Style.RESET_ALL, "Во время открытия страницы произошла ошибка!", sep='')
        return False


   
def create(driver, domain, text1, text2):
    try:
        driver.get(f"{domain}/add_member")
        input_name = driver.find_element(
            By.XPATH, 
            "//input[@name='name' and @placeholder='Введите имя' and @class='form-control']"
        )
        input_address = driver.find_element(
            By.XPATH, 
            "//input[@name='address' and @placeholder='Введите адрес' and @class='form-control']"
        )
    
  
        params_dict = {
                "name": text1,
                "address": text2,
        }
    
        input_name.send_keys(params_dict["name"])
        input_address.send_keys(params_dict["address"])
    
        element = driver.find_element(By.XPATH, "//button[@class='btn btn-success' and @type='submit' and text()='Добавить']")
    
        driver.execute_script(
            "arguments[0].scrollIntoView();", 
            element
        )
        time.sleep(1)
        element.click()
        
        print(Fore.GREEN, f"\rНовый член комиссии {text1} успешно создан", Style.RESET_ALL, Fore.CYAN)
    
        return True
    except:
        print(Fore.RED,"ERROR:", Style.RESET_ALL, "Во время создания нового члена комиссии произошла ошибка!", sep='')
        return False


def check(driver, domain, text1):
    try:
        driver.get(f"{domain}/municipal_members")
        span_element = driver.find_element(By.XPATH, f"//ul/li/strong[text()='{text1}']")
        time.sleep(1)
        if span_element.text == text1:
            print(Fore.GREEN, f"\rНовый член комиссии {text1} найден в списках", Style.RESET_ALL, Fore.CYAN)
            return True
        else:
            print(Fore.RED,"ERROR:", Style.RESET_ALL, f"Новый член комиссии {text1} не найден!", sep='')
            return False
    except:
        print(Fore.RED,"ERROR:", Style.RESET_ALL, f"Новый член комиссии {text1} не найден!", sep='')
        return False
