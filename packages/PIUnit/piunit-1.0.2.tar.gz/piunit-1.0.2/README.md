# PIUnit

Добавляет возможность тестировать код с функциями print и input

<pre>
Описание методов класса BasePIUnitTest:
+ test_print(test_func: Callable, prints: SupportsIndex,
                   all_: bool = False)
  
  Тестирует код с функцией print.
    Проверяет, напечаталось ли в print то, что ожидалось.
    Args:
      test_func: Callable (тестируемый объект)
      prints: SupportsIndex (значения для print)
      all_: bool (при True - вернёт ошибку если остались неиспользованные
        значения)


+ test_input(test_func: Callable, inputs: SupportsIndex,
                   all_: bool = False)

  Тестирует код с функцией input.
  Возвращает указанные данные при вызове input.

  Args:
    test_func: Callable (тестируемый объект)
    inputs: SupportsIndex (значения для input)
    all_: bool (при True, вернёт ошибку если остались неиспользованные
    значения)


+ test_print_input(self, test_func: Callable,
                         inputs: SupportsIndex,
                         prints: SupportsIndex,
                         all_: bool = False
                         ):

  Тестирует код с функцией print и input.

  Подставляет по порядку данные из prints и inputs.

  Args:
    test_func: Callable (тестируемый объект)
    inputs: SupportsIndex (значения для input)
    prints: SupportsIndex (значения для print)
    all_: bool (при True, вернёт ошибку если остались неиспользованные
    значения)
</pre>

## Использованные технологии: 


![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/unittest-%23000.svg?style=for-the-badge&logoColor=white)
<br><br>

## Прежде всего:

> Установите Python (если он не установлен)<br>
> [Скачать Python3](https://www.python.org/downloads/)

<br>

Клонируйте репозиторий и перейдите в установленную директорию:
```
git clone https://github.com/Ryize/PIUnit.git
cd PIUnit
```

<br>

Пример использования:
```
from main import print_hello_world, log_user_state, get_data
from test import BasePIUnitTest


class TestOne(BasePIUnitTest):
    def test_one(self):
        self.test_print(print_hello_world, ['Hello, World!'])
        self.test_input(log_user_state, ['Смена пароля', 'Пароль успешно изменён'], True)
        self.test_print_input(get_data, [10, 3, 2], ['Результат выполнения кода: 15'])
```

> Технологии, использованные в проекте: Python 3, unittest
