from time import sleep
from colorama import Fore, Style


# Ширина рамки
width_init = 80

color_list = [
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTCYAN_EX, 
]

def border():
    for i in range(width_init):
        print('*', end='')
    else:
        print()


def line(text=''):
    # Проверка на длину максимально, вместимую в рамку
    if len(text) <= width_init:
        # Если параметра нет, то вывод пустой части рамки
        if text == '':
            for i in range(width_init):
                if i == 0 or i+1 == width_init:
                    print('*', end='')
                else:
                    print(' ', end='')
            else:
                print()
        # Если параметр есть, то он выводится по центру
        else:
            len_text = len(text)
            # Центрирование текста
            index_start = int((width_init - len_text) / 2)
            # Для отслеживания позиции в тексте параметра
            pos = 0
            for i in range(width_init):
                # Если начальный или конечный элемента
                if i == 0 or i+1 == width_init:
                    print('*', end='')
                elif i == index_start:
                    pos = 0
                    print(text[pos], end='')
                elif i > index_start and pos + 1 < len_text:
                    pos += 1
                    print(text[pos], end='')
                else:
                    print(' ', end='')
            else:
                print()
    else:
        print('ERROR! Ошибка при выводе строки.')


def phase(index:int, text:str) -> None:
    """Печать информации о фазе

        Информация о индексе и названии фазы выводятся пользователю.

        Аргументы:
            index: индекс фазы
            text: название фазы

        Возвращаемое значение:
            Отсутствует
    """
    # Простой отступ с настройкой окраски рамки
    print(color_list[index%len(color_list)])
    # Верхняя рамка
    border()
    line()
    line(f'Фаза {index}')
    line()
    line(text)
    line()
    # Нижняя рамка
    border()
    # Сброс цветовой настройки
    print(Style.RESET_ALL)

def about_test():
    print('\n\n\n', Fore.YELLOW)
    print("Программа автоматического тестирования проекта")
    print("Автор: Вертаева Виктория Валерьевна")
    print("Группа: 221-351")
    print("Версия: 1.0")
    print("Дата создания: 29-11-2024")
    print(Style.RESET_ALL, '\n\n\n')

    for i in range(10):
        sleep(0.3)
        print("\rЗапуск авто-тестирования" + "."*i, end='')
    
    print()

