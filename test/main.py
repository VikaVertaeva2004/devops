from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# Подключаем разделы для тестирования
from utilities import phase, about_test
from test_func import open_page, create, check
from faker import Faker
fake = Faker()


def auto_test():
   options = webdriver.ChromeOptions()

   options.add_argument("start-maximized");
   options.add_argument("disable-infobars");
   options.add_argument("--disable-extensions");
   options.add_argument("--disable-gpu");
   options.add_argument("--disable-dev-shm-usage");
   options.add_argument("--no-sandbox")
   # service=ChromeService(ChromeDriverManager(driver_version="131.0.6778.85").install()), options=options 
   driver = webdriver.Chrome()

   # driver.maximize_window()
   driver.implicitly_wait(10)
   
   domain = "http://192.168.50.30:9876"

   driver.get(domain)

   index = 1

   phase(index, "Тестирование открытия страницы.")
   result_test_1 = open_page(driver)
   assert result_test_1 == True, "Ошибка при открытии страницы."
   index +=1
   
   text1 = fake.name_female()
   text2 = fake.name_female()
   phase(index, "Тестирование формы добавления нового члена комисии.")
   result_test_1 = create(driver, domain, text1, text2)
   assert result_test_1 == True, "Новый член комиссии не создан"
   index +=1

   phase(index, f"Проверка на наличие записи о новом члене комисии {text1}.")
   result_test_1 = check(driver, domain, text1)
   assert result_test_1 == True, f"Запись о новом члене комисии {text1} не найдена в базе данных"
   index +=1

   driver.close()
   driver.quit()

def main():
   about_test()
   auto_test()
   print('\n\n\n')

main()
