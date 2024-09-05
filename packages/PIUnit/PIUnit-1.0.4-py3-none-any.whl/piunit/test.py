from typing import Callable, Iterable, SupportsIndex
from unittest import TestCase


class PrintError(AssertionError):
    pass


class ManyPrintArgsError(PrintError):
    pass


class ZeroPrintArgsError(PrintError):
    pass


class InputError(AssertionError):
    pass


class ManyInputArgsError(InputError):
    pass


class ZeroInputArgsError(PrintError):
    pass


class NoMatchPrintError(PrintError):
    pass


class BasePIUnitTest(TestCase):
    __print = print
    __input = input

    def test_print(self, test_func: Callable, prints: SupportsIndex,
                   all_: bool = False, *args, **kwargs) -> None:
        """
        Тестирует код с функцией print.

        Проверяет, напечаталось ли в print то, что ожидалось.

        Args:
            test_func: Callable (тестируемый объект)
            prints: SupportsIndex (значения для print)
            all_: bool (при True, вернёт ошибку если остались неиспользованные
             значения)
        """
        self.__prints = prints
        __builtins__['print'] = self.__fake_print
        test_func(*args, **kwargs)
        if all_ and self.__prints:
            raise ManyPrintArgsError('Использованы не все значения print')
        __builtins__['print'] = self.__print

    def test_input(self, test_func: Callable, inputs: SupportsIndex,
                   all_: bool = False, *args, **kwargs) -> None:
        """
        Тестирует код с функцией input.

        Возвращает указанные данные при вызове input.

        Args:
            test_func: Callable (тестируемый объект)
            inputs: SupportsIndex (значения для input)
            all_: bool (при True, вернёт ошибку если остались неиспользованные
            значения)
        """
        self.__inputs = inputs
        __builtins__['input'] = self.__fake_input
        test_func(*args, **kwargs)
        if all_ and self.__inputs:
            raise ManyInputArgsError('Использованы не все значения input')
        __builtins__['input'] = self.__input

    def test_print_input(self, test_func: Callable,
                         inputs: SupportsIndex,
                         prints: SupportsIndex,
                         all_: bool = False,
                         *args,
                         **kwargs) -> None:
        """
        Тестирует код с функцией print и input.

        Подставляет по порядку данные из prints и inputs.

        Args:
            test_func: Callable (тестируемый объект)
            inputs: SupportsIndex (значения для input)
            prints: SupportsIndex (значения для print)
            all_: bool (при True, вернёт ошибку если остались неиспользованные
            значения)
        """
        self.__prints = prints
        self.__inputs = inputs

        __builtins__['print'] = self.__fake_print
        __builtins__['input'] = self.__fake_input

        test_func(*args, **kwargs)

        if all_ and self.__inputs:
            raise ManyInputArgsError('Использованы не все значения input')
        if all_ and self.__prints:
            raise ManyPrintArgsError('Использованы не все значения print')

        __builtins__['print'] = self.__print
        __builtins__['input'] = self.__input

    def __fake_input(self, *args, **kwargs):
        if not self.__inputs:
            raise ZeroInputArgsError('Нет значений для подстановки в input')
        return self.__inputs.pop(0)

    def __fake_print(self, *args, **kwargs):
        if not args:
            args = ['\n']

        if not len(self.__prints):
            raise ZeroPrintArgsError(
                'Нет значений для подстановки в print')
        if len(args) == 1:
            value = args[0]
        else:
            value = kwargs.get('sep', ' ').join(map(str, args))
        if not value == self.__prints[0]:
            raise NoMatchPrintError(
                f'Указанное и полученное значение различается. {value} != {self.__prints[0]}')
        del self.__prints[0]
